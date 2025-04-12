# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Definitions for forecasting metrics."""
import logging
from abc import abstractmethod
from collections import OrderedDict
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import numpy as np
import pandas as pd
from scipy.stats import norm

from azureml._common._error_definition.azureml_error import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    TimeseriesTableTrainAbsent,
    TimeseriesTableGrainAbsent,
    TimeseriesTableValidAbsent)
from azureml.automl.core.shared.exceptions import DataErrorException,\
    ClientException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from . import _regression, _scoring_utilities, constants
from ._metric_base import Metric, NonScalarMetric
from ..featurization.timeseries.timeseries_transformer import TimeSeriesTransformer
from azureml.automl.core.shared.exceptions import ClientException
from azureml.automl.runtime.shared.score._regression import NormRMSE
from azureml.automl.core.shared.constants import TimeSeriesInternal, AggregationFunctions
from azureml.automl.core.shared._diagnostics.contract import Contract

_logger = logging.getLogger(__name__)


class ForecastingMetric(Metric):
    """Abstract class for forecast metrics."""

    y_pred_str = "y_pred"
    y_test_str = "y_test"

    @staticmethod
    def convert_to_list_of_str(val: Union[Any, Tuple[Any], List[Any]]) -> List[str]:
        """
        Convert an input to a list of str.

        Useful for converting grain column names or values to a list of strings.
        """
        val_collection = val if isinstance(val, list) or isinstance(val, tuple) else [val]
        return list(map(str, val_collection))

    def __init__(
        self,
        y_test: np.ndarray,
        y_pred: np.ndarray,
        horizons: np.ndarray,
        y_min: Optional[float] = None,
        y_max: Optional[float] = None,
        y_std: Optional[float] = None,
        bin_info: Optional[Dict[str, float]] = None,
        sample_weight: Optional[np.ndarray] = None,
        X_test: Optional[pd.DataFrame] = None,
        X_train: Optional[pd.DataFrame] = None,
        y_train: Optional[np.ndarray] = None,
        grain_column_names: Optional[List[str]] = None,
        time_column_name: Optional[str] = None,
        origin_column_name: Optional[Any] = None
    ) -> None:
        """
        Initialize the forecasting metric class.

        :param y_test: True labels for the test set.
        :param y_pred: Predictions for each sample.
        :param horizons: The integer horizon alligned to each y_test. These values should be computed
            by the timeseries transformer. If the timeseries transformer does not compute a horizon,
            ensure all values are the same (ie. every y_test should be horizon 1.)
        :param y_min: Minimum target value.
        :param y_max: Maximum target value.
        :param y_std: Standard deviation of the targets.
        :param bin_info: Metadata about the dataset (required for nonscalar metrics).
        :param sample_weight: Weighting of each sample in the calculation.
        :param X_test: The inputs which were used to compute the predictions.
        :param X_train: The inputs which were used to train the model.
        :param y_train: The targets which were used to train the model.
        :param grain_column_names: The grain column name.
        :param time_column_name: The time column name.
        :param origin_column_name: The origin time column name.
        """
        if y_test.shape[0] != y_pred.shape[0]:
            raise DataErrorException(
                "Mismatched input shapes: y_test={}, y_pred={}".format(y_test.shape, y_pred.shape),
                target="y_pred", reference_code="_forecasting.ForecastingMetric.__init__",
                has_pii=True).with_generic_msg("Mismatched input shapes: y_test, y_pred")
        self._y_test = y_test
        self._y_pred = y_pred
        self._horizons = horizons
        self._y_min = y_min
        self._y_max = y_max
        self._y_std = y_std
        self._bin_info = bin_info
        self._sample_weight = sample_weight
        self._X_test = X_test
        self._X_train = X_train
        self._y_train = y_train
        self._grain_column_names = grain_column_names
        self._time_column_name = time_column_name
        self._origin_column_name = origin_column_name

        super().__init__()

    @abstractmethod
    def compute(self) -> Dict[str, Any]:
        """Compute the score for the metric."""
        ...

    def _group_raw_by_horizon(self) -> Dict[int, Dict[str, List[float]]]:
        """
        Group y_true and y_pred by horizon.

        :return: A dictionary of horizon to y_true, y_pred.
        """
        grouped_values = {}  # type: Dict[int, Dict[str, List[float]]]
        for idx, h in enumerate(self._horizons):
            if h in grouped_values:
                grouped_values[h][ForecastingMetric.y_pred_str].append(self._y_pred[idx])
                grouped_values[h][ForecastingMetric.y_test_str].append(self._y_test[idx])
            else:
                grouped_values[h] = {
                    ForecastingMetric.y_pred_str: [self._y_pred[idx]],
                    ForecastingMetric.y_test_str: [self._y_test[idx]],
                }

        return grouped_values

    @staticmethod
    def _group_scores_by_horizon(score_data: List[Dict[int, Dict[str, Any]]]) -> Dict[int, List[Any]]:
        """
        Group computed scores by horizon.

        :param score_data: The dictionary of data from a cross-validated model.
        :return: The data grouped by horizon in sorted order.
        """
        grouped_data = {}  # type: Dict[int, List[Any]]
        for cv_fold in score_data:
            for horizon in cv_fold.keys():
                if horizon in grouped_data.keys():
                    grouped_data[horizon].append(cv_fold[horizon])
                else:
                    grouped_data[horizon] = [cv_fold[horizon]]

        # sort data by horizon
        grouped_data_sorted = OrderedDict(sorted(grouped_data.items()))
        return grouped_data_sorted


class ForecastMAPE(ForecastingMetric, NonScalarMetric):
    """Mape Metric based on horizons."""

    SCHEMA_TYPE = constants.SCHEMA_TYPE_MAPE
    SCHEMA_VERSION = "1.0.0"

    MAPE = "mape"
    COUNT = "count"

    def compute(self) -> Dict[str, Any]:
        """Compute mape by horizon."""
        grouped_values = self._group_raw_by_horizon()
        for h in grouped_values:
            partial_pred = np.array(grouped_values[h][ForecastingMetric.y_pred_str])
            partial_test = np.array(grouped_values[h][ForecastingMetric.y_test_str])

            self._data[h] = {
                ForecastMAPE.MAPE: _regression._mape(partial_test, partial_pred),
                ForecastMAPE.COUNT: len(partial_pred),
            }

        ret = NonScalarMetric._data_to_dict(ForecastMAPE.SCHEMA_TYPE, ForecastMAPE.SCHEMA_VERSION, self._data)
        return cast(Dict[str, Any], _scoring_utilities.make_json_safe(ret))

    @staticmethod
    def aggregate(scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Fold several scores from a computed metric together.

        :param scores: List of computed scores.
        :return: Aggregated score.
        """
        if not Metric.check_aggregate_scores(scores, constants.FORECASTING_MAPE):
            return NonScalarMetric.get_error_metric()

        score_data = [score[NonScalarMetric.DATA] for score in scores]
        grouped_data = ForecastingMetric._group_scores_by_horizon(score_data)

        data = {}
        for horizon in grouped_data:
            agg_count = 0
            agg_mape = 0.0
            folds = grouped_data[horizon]
            for fold in folds:
                fold_count = fold[ForecastMAPE.COUNT]
                agg_count += fold_count
                agg_mape += fold[ForecastMAPE.MAPE] * fold_count
            agg_mape = agg_mape / agg_count
            data[horizon] = {ForecastMAPE.MAPE: agg_mape, ForecastMAPE.COUNT: agg_count}

        ret = NonScalarMetric._data_to_dict(ForecastMAPE.SCHEMA_TYPE, ForecastMAPE.SCHEMA_VERSION, data)
        return cast(Dict[str, Any], _scoring_utilities.make_json_safe(ret))


class ForecastResiduals(ForecastingMetric, NonScalarMetric):
    """Forecasting residuals metric."""

    SCHEMA_TYPE = constants.SCHEMA_TYPE_RESIDUALS
    SCHEMA_VERSION = "1.0.0"

    EDGES = "bin_edges"
    COUNTS = "bin_counts"
    MEAN = "mean"
    STDDEV = "stddev"
    RES_COUNT = "res_count"

    def compute(self) -> Dict[str, Any]:
        """Compute the score for the metric."""
        if self._y_std is None:
            raise DataErrorException(
                "y_std required to compute Residuals",
                target="_y_std", reference_code="_forecasting.ForecastResiduals.compute",
                has_pii=False)

        num_bins = 10
        # If full dataset targets are all zero we still need a bin
        y_std = self._y_std if self._y_std != 0 else 1

        self._data = {}
        grouped_values = self._group_raw_by_horizon()
        for h in grouped_values:
            self._data[h] = {}
            partial_residuals = np.array(grouped_values[h][ForecastingMetric.y_pred_str]) - np.array(
                grouped_values[h][ForecastingMetric.y_test_str]
            )
            mean = np.mean(partial_residuals)
            stddev = np.std(partial_residuals)
            res_count = len(partial_residuals)

            counts, edges = _regression.Residuals._hist_by_bound(partial_residuals, 2 * y_std, num_bins)
            _regression.Residuals._simplify_edges(partial_residuals, edges)
            self._data[h][ForecastResiduals.EDGES] = edges
            self._data[h][ForecastResiduals.COUNTS] = counts
            self._data[h][ForecastResiduals.MEAN] = mean
            self._data[h][ForecastResiduals.STDDEV] = stddev
            self._data[h][ForecastResiduals.RES_COUNT] = res_count

        ret = NonScalarMetric._data_to_dict(
            ForecastResiduals.SCHEMA_TYPE, ForecastResiduals.SCHEMA_VERSION, self._data
        )
        return cast(Dict[str, Any], _scoring_utilities.make_json_safe(ret))

    @staticmethod
    def aggregate(scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Fold several scores from a computed metric together.

        :param scores: List of computed scores.
        :return: Aggregated score.
        """
        if not Metric.check_aggregate_scores(scores, constants.FORECASTING_RESIDUALS):
            return NonScalarMetric.get_error_metric()

        score_data = [score[NonScalarMetric.DATA] for score in scores]
        grouped_data = ForecastingMetric._group_scores_by_horizon(score_data)

        data = {}
        for horizon in grouped_data:
            # convert data to how residuals expects
            partial_scores = [{NonScalarMetric.DATA: fold_data} for fold_data in grouped_data[horizon]]
            # use aggregate from residuals
            data[horizon] = _regression.Residuals.aggregate(partial_scores)[NonScalarMetric.DATA]

        ret = NonScalarMetric._data_to_dict(ForecastResiduals.SCHEMA_TYPE, ForecastResiduals.SCHEMA_VERSION, data)
        return cast(Dict[str, Any], _scoring_utilities.make_json_safe(ret))


class ForecastAdjustmentResiduals(ForecastingMetric, NonScalarMetric):
    SCHEMA_TYPE = constants.SCHEMA_TYPE_GAP_ADJUSTMENT_TABLE
    SCHEMA_VERSION = '1.0.0'

    def compute(self) -> Dict[str, Any]:
        """ This code will be executed for each CV fold"""
        if self._X_test is None or self._y_test is None or self._y_pred is None:
            raise ClientException._with_error(
                AzureMLError.create(
                    TimeseriesTableValidAbsent,
                    target="_valid_data",
                    reference_code=ReferenceCodes._TS_METRIX_NO_VALID))
        # Creating CV data
        df_valid = self._X_test.index.to_frame(index=False)
        df_valid['y_true'] = self._y_test
        df_valid['y_pred'] = self._y_pred
        df_train = self._X_train.index.to_frame(index=False)
        df_train['y_true'] = self._y_train

        groupby_valid = df_valid.groupby(self._grain_column_names)
        groupby_train = df_train.groupby(self._grain_column_names)  # For min and max values for nrmse
        grain_column_names = self.convert_to_list_of_str(self._grain_column_names)
        grains_data = []
        for grain, df_one_valid in groupby_valid:
            grain_dict = {}
            grain_vals = self.convert_to_list_of_str(grain)
            grain_dict[TimeSeriesInternal.GRAIN_VALUE] = grain_vals

            if df_one_valid is not np.empty:
                y_true = df_one_valid['y_true'].astype(float).values
                y_pred = df_one_valid['y_pred'].astype(float).values
                train_min, train_max = list(groupby_train.get_group(grain)['y_true'].agg([AggregationFunctions.MIN,
                                            AggregationFunctions.MAX]))
                cv_nrmse = (round(NormRMSE(y_true, y_pred, train_max, train_min).compute(), 5))
                grain_dict[TimeSeriesInternal.GAP_CV_NRMSE] = round(cv_nrmse, 5)
                pred_gap = y_pred - y_true
                cv_bias_percent = max(np.where(pred_gap > 0, 1, 0).sum(),
                                      np.where(pred_gap < 0, 1, 0).sum()) / len(pred_gap)
                grain_dict[TimeSeriesInternal.GAP_CV_BIAS] = round(cv_bias_percent, 5)

                # convert time column to "iso" format and extract the last train_length values
                grain_dict[TimeSeriesInternal.MAX_TIME] = df_one_valid[self._time_column_name].max().isoformat()
            grains_data.append(grain_dict)
        self._data = {TimeSeriesInternal.GRAIN_DATA: grains_data,
                      TimeSeriesInternal.GRAIN_COL_NAME: grain_column_names}
        ret = NonScalarMetric._data_to_dict(
            ForecastAdjustmentResiduals.SCHEMA_TYPE,
            ForecastAdjustmentResiduals.SCHEMA_VERSION,
            self._data)
        return cast(Dict[str, Any], _scoring_utilities.make_json_safe(ret))

    @staticmethod
    def aggregate(
        scores: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Fetch the last CV data
        :param scores: List of computed table metrics.
        :return: last CV Data
        """
        _logger.info("Starting to aggregate the CV data for gap analysis")
        gap_last_cv = {}
        last_CV_num = 0
        # Identifying the latest cv fold from the max date of the first grain
        gap_last_cv_dt: Dict = None
        max_date = str(pd.Timestamp.min)
        arbitrary_grain = None
        for cv_num, score in enumerate(scores):
            cv = score[NonScalarMetric.DATA]
            arbitrary_CV_data = None
            for cv_data in cv[TimeSeriesInternal.GRAIN_DATA]:
                if not arbitrary_grain:
                    arbitrary_grain = cv_data[TimeSeriesInternal.GRAIN_VALUE]
                if cv_data[TimeSeriesInternal.GRAIN_VALUE] == arbitrary_grain:
                    arbitrary_CV_data = cv_data
                    break

            Contract.assert_value(arbitrary_CV_data, "Same grain not found in all CV folds",
                                  reference_code=ReferenceCodes._TS_GRAIN_ABSENT_CV_FOLD)
            if max_date <= arbitrary_CV_data[TimeSeriesInternal.MAX_TIME]:
                max_date = arbitrary_CV_data[TimeSeriesInternal.MAX_TIME]
                gap_last_cv_dt = cv
                last_CV_num = cv_num

            Contract.assert_value(gap_last_cv_dt, "Max date could not be found",
                                  reference_code=ReferenceCodes._TS_MAX_DATE_NOT_FOUND)

        gap_last_cv = {TimeSeriesInternal.GAP_CV_METRIC: gap_last_cv_dt,
                       TimeSeriesInternal.LAST_CV_NUM: last_CV_num}

        ret = NonScalarMetric._data_to_dict(
            ForecastAdjustmentResiduals.SCHEMA_TYPE,
            ForecastAdjustmentResiduals.SCHEMA_VERSION,
            gap_last_cv)

        _logger.info("Captured last CV data for gap analysis {}".format(last_CV_num))
        return cast(Dict[str, Any], _scoring_utilities.make_json_safe(ret))


class ForecastTable(ForecastingMetric, NonScalarMetric):
    """The table, containing the list of true and predicted values."""
    SCHEMA_TYPE = constants.SCHEMA_TYPE_FORECAST_HORIZON_TABLE
    SCHEMA_VERSION = '1.0.0'
    MAX_CROSS_VALIDATION_FOLDS = 5
    MAX_FORECAST_TRAIN_DATA_POINTS = 20  # Showing at most 20 training data points
    MAX_FORECAST_VALID_DATA_POINTS = 80  # limited by UI, showing up to 80 validate data points per grain
    MAX_FORECAST_GRAINS = 20

    def compute(self) -> Dict[str, Any]:
        """ Gather train table metrics for a single fold"""
        if self._X_train is None or self._y_train is None:
            raise ClientException._with_error(
                AzureMLError.create(
                    TimeseriesTableTrainAbsent,
                    target="_train_data",
                    reference_code=ReferenceCodes._TS_METRIX_NO_TRAIN))

        if self._grain_column_names is None:
            raise ClientException._with_error(
                AzureMLError.create(
                    TimeseriesTableGrainAbsent,
                    target="_grain_column_name",
                    reference_code=ReferenceCodes._TS_METRIX_NO_GRAIN))

        if self._X_test is None or self._y_test is None or self._y_pred is None:
            raise ClientException._with_error(
                AzureMLError.create(
                    TimeseriesTableValidAbsent,
                    target="_valid_data",
                    reference_code=ReferenceCodes._TS_METRIX_NO_VALID))
        # time col and grain col are stored in index
        df_train = self._X_train.index.to_frame(index=False)
        df_train['y_true'] = self._y_train

        df_valid = self._X_test.index.to_frame(index=False)
        df_valid['y_true'] = self._y_test
        df_valid['y_pred'] = self._y_pred
        groupby_valid = df_valid.groupby(self._grain_column_names)

        grain_column_names = self.convert_to_list_of_str(self._grain_column_names)
        self._data = {'time': [],
                      'grain_names': grain_column_names,
                      'grain_value_list': [],
                      'y_true': [],
                      'y_pred': [],
                      'PI_upper_bound': [],
                      'PI_lower_bound': []
                      }
        # For UI purpose, we are calculateing intervals for each fold using the residuals from each fold, in sequence.
        # But these estimates are likely to be noisy because we can't calculate PIs until we have predictions
        # from all cv folds which is the nature of the estimation process.
        z_score = norm.ppf(0.05)
        for igrain, (grain, df_one_train) in enumerate(df_train.groupby(grain_column_names)):
            # If user has provided the valid data set, missing given grain,
            # do not show it in the visual.
            if grain not in groupby_valid.groups.keys():
                continue
            # add built-in mechanism for lowering the cap on grains
            if igrain >= ForecastTable.MAX_FORECAST_GRAINS:
                break
            df_one_valid = groupby_valid.get_group(grain)
            # We may have introduced multiple horizons during training, here we are
            # removing it.
            # For validation set the horizons were already removed.
            if self._origin_column_name and self._origin_column_name in df_train.columns:
                df_one_train.set_index([self._time_column_name, self._origin_column_name], inplace=True)
                df_one_train = TimeSeriesTransformer.select_latest_origin_dates(
                    df_one_train,
                    time_column_name=cast(str, self._time_column_name),
                    time_series_id_column_names=[],
                    # df_one_train contains only one grain, so we do not need to set it.
                    origin_column_name=cast(str, self._origin_column_name))
                df_one_train.reset_index(inplace=True, drop=False)

            df_one_train.sort_values(by=self._time_column_name, ascending=True, inplace=True)

            df_one_train_trimmed = df_one_train.iloc[-ForecastTable.MAX_FORECAST_TRAIN_DATA_POINTS:]
            df_one_valid = df_one_valid.iloc[:ForecastTable.MAX_FORECAST_VALID_DATA_POINTS]
            df_one = pd.concat([df_one_train_trimmed, df_one_valid], sort=False, ignore_index=True)

            grain_vals = self.convert_to_list_of_str(grain)

            self._data['grain_value_list'].append(grain_vals)

            y_true_list = list(df_one_valid['y_true'].astype(float).values)
            y_pred_list = list(df_one_valid['y_pred'].astype(float).values)
            stddev = np.std([a - b for a, b in zip(y_true_list, y_pred_list)])  # compute std(y_true, y_pred)
            if stddev == 0:
                # If all residuals are the same, we will clculate the residuals of training set.
                resid_train = df_one_train['y_true'].values - y_pred_list[-1]
                stddev = np.std(resid_train)
            # we introduce horizon in PI computation since the further the forecast date,
            # the less confident of the prediction we have.
            ci_bound = abs(z_score * stddev * np.sqrt(np.arange(1, len(y_pred_list) + 1)))
            PI_upper_bound = [a + b for a, b in zip(y_pred_list, ci_bound)]
            PI_lower_bound = [a - b for a, b in zip(y_pred_list, ci_bound)]
            self._data['y_true'].append(round(df_one['y_true'], 2).astype(float).values)
            self._data['y_pred'].append(y_pred_list)
            self._data['PI_upper_bound'].append(PI_upper_bound)
            self._data['PI_lower_bound'].append(PI_lower_bound)

            # convert time column to "iso" format and extract the last train_length values
            self._data['time'].append(list(df_one[self._time_column_name].apply(lambda x: x.isoformat())))

        ret = NonScalarMetric._data_to_dict(
            ForecastTable.SCHEMA_TYPE,
            ForecastTable.SCHEMA_VERSION,
            self._data)
        return cast(Dict[str, Any], _scoring_utilities.make_json_safe(ret))

    @staticmethod
    def aggregate(
        scores: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Fold several scores from a computed metric together.

        :param scores: List of computed table metrics.
        :return: Aggregated table metrics.
        """
        if not Metric.check_aggregate_scores(scores, constants.FORECASTING_TABLE):
            return NonScalarMetric.get_error_metric()

        score_data = [score[NonScalarMetric.DATA] for score in scores][:ForecastTable.MAX_CROSS_VALIDATION_FOLDS]
        # only store up to 5 folds data

        ret = NonScalarMetric._data_to_dict(
            ForecastTable.SCHEMA_TYPE,
            ForecastTable.SCHEMA_VERSION,
            score_data)
        return cast(Dict[str, Any], _scoring_utilities.make_json_safe(ret))
