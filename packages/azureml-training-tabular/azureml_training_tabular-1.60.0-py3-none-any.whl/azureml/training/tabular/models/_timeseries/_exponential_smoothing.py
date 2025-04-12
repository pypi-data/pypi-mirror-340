# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The wrapper for Exponential Smoothing models."""

import logging
from itertools import product
from typing import Any, Dict, cast

import numpy as np
import pandas as pd
import statsmodels.tsa.holtwinters as holtwinters

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared import constants, exceptions, logging_utilities
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.types import GrainType
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    AutoMLInternalLogSafe,
    ForecastingExpoSmoothingNoModel,
    TimeseriesDfInvalidArgForecastHorizon
)
from azureml.automl.core.shared._diagnostics.contract import Contract

from ...timeseries._time_series_data_set import TimeSeriesDataSet
from ._multi_grain_forecast_base import _MultiGrainForecastBase

logger = logging.getLogger(__name__)


class ExponentialSmoothing(_MultiGrainForecastBase):
    """ExponentialSmoothing multigrain forecasting model."""

    def __init__(self, timeseries_param_dict: Dict[str, Any]):
        """Create an ExponentialSmoothing multi-grain forecasting model."""
        super().__init__(timeseries_param_dict)

        self.seasonality = timeseries_param_dict.get(
            constants.TimeSeries.SEASONALITY, constants.TimeSeriesInternal.SEASONALITY_VALUE_NONSEASONAL
        )
        Contract.assert_true(
            isinstance(self.seasonality, int) and self.seasonality >= 1,
            "Seasonality is not a positive integer.",
            log_safe=True,
        )

    def _fit_in_sample_single_grain_impl(
        self, model: Any, grain_level: GrainType, X_grain: TimeSeriesDataSet
    ) -> np.ndarray:
        """
        Retreive in sample fitted values on a single grain from Exponential Smoothing model.

        :param: model: The Exponential Smoothing model.
        :type model: Any.
        :param grain_level: The name of a grain.
        :type grain_level: GrainType.
        :param X_grain: The training data from a single grain.
        :type X_grain: TimeSeriesDataSet.
        :returns: In sample fitted values on a single grain from Exponential Smoothing model.
        :type: np.ndarry.

        """

        date_filter = X_grain.time_index.values
        date_argmax = self._get_date_argmax_safe(date_filter=date_filter)
        date_range = pd.date_range(
            start=self._first_observation_dates[grain_level], end=date_filter[date_argmax], freq=self._freq
        )

        index = np.searchsorted(date_range, date_filter)

        # statsmodels is buggy - so catch exceptions here and default to returning zeros for in-sample preds
        # in-sample predictions are not essential for selection or forecasting so this is the least bad option
        # Don't return NaNs because the runner fails if predictions contain NaN values.
        try:
            pred = model.fittedvalues
        except Exception as ex_na_in_sample_pred:
            pred = np.zeros(date_range.shape[0])
            logger.warning("In sample prediction from Exponential Smoothing fails, and NA's are imputed as zeros.")
            logging_utilities.log_traceback(ex_na_in_sample_pred, logger, is_critical=False)

        # In case of unforeseen statsmodels bugs around in-sample prediction,
        # check if we will request invalid indices and prepend zeros if so.
        max_index = index.max()
        if pred.size <= max_index:
            n_more_padding = max_index - pred.size + 1
            more_padding = np.zeros(n_more_padding)
            pred = np.nan_to_num(np.concatenate((more_padding, pred)), copy=False)

        # In case of the in sample prediction of statsmodels didn't fail completely,
        # but still produces some NA's, cast those NA's to zeros.
        return cast(np.ndarray, np.nan_to_num(pred[index], copy=False))

    def _get_forecast_single_grain_impl(
        self, model: Any, max_horizon: int, grain_level: GrainType, X_pred_grain: TimeSeriesDataSet
    ) -> np.ndarray:
        """
        Forecast on a single grain from Exponential Smoothing model.

        :param: model: The Exponential Smoothing model.
        :type model: Any.
        :param max_horizon: The maximum horizon of the forecast.
        :type: max_horizon: int.
        :param grain_level: The name of a grain.
        :type grain_level: GrainType
        :param X_pred_grain: The data frame with one grain.
        :type X_pred_grain: TimeSeriesDataSet
        :returns: The forecast on a single grain from Exponential smoothing model.
        :type: np.ndarray

        """

        # ExponentialSmoothing needs to have a meaningful max horizon
        if max_horizon <= 0:
            raise exceptions.DataException._with_error(
                AzureMLError.create(
                    TimeseriesDfInvalidArgForecastHorizon,
                    reference_code=ReferenceCodes._TSDF_INVALID_ARG_MAX_HORIZON_VAL3
                )
            )

        # Impute NA's in forecast with 0 for now
        pred = np.nan_to_num(model.forecast(steps=int(max_horizon)), copy=False)

        return self.align_out(
            in_sample=False,
            pred=pred,
            X_pred_grain=X_pred_grain,
            X_fit_grain=X_pred_grain.concat([]),
            max_horizon=max_horizon,
            freq=self._freq,
        )

    def _model_selection_exponential_smoothing(self, X_pred_grain: pd.DataFrame, grain_level: GrainType) -> Any:
        """
        Select the best model from a family of Exponential Smoothing models on one grain,
        by Corrected Akaike's Information Criterion (AICc).

        :param X_pred_grain: The data frame with one grain.
        :type X_pred_grain: pd.DataFrame
        :param grain_level: The name of a grain.
        :type: grain_level: GrainType
        :returns: The Exponential smoothing model.
        :type: Any.
        """

        series_values = X_pred_grain.get(constants.TimeSeriesInternal.DUMMY_TARGET_COLUMN).values.astype(float)

        # Internal function for fitting a statsmodel ExponentialSmoothing model
        #  and determining if a model type should be considered in selection
        # ------------------------------------------------------------------

        def fit_sm(model_type):
            trend_type, seas_type, damped = model_type

            char_to_statsmodels_opt = {"A": "add", "M": "mul", "N": None}
            exponential_smoothing_model = holtwinters.ExponentialSmoothing(
                series_values,
                trend=char_to_statsmodels_opt[trend_type],
                seasonal=char_to_statsmodels_opt[seas_type],
                damped_trend=damped,
                seasonal_periods=self.seasonality,
                initialization_method=None,
            )
            try:
                return exponential_smoothing_model.fit()
            except Exception as ex_model_fit_fail:
                logger.warning(
                    "Fitting of an individual exponential smoothing model failed (model selection could still "
                    "be successful if there is at least one successful fit from a family of models.)"
                )
                logging_utilities.log_traceback(ex_model_fit_fail, logger, is_critical=False)

        def model_is_valid(model_type, not_all_values_gt_zero):
            trend_type, seas_type, damped = model_type

            if trend_type == "N" and damped:
                return False

            if (trend_type == "M" or seas_type == "M") and not_all_values_gt_zero:
                return False

            return True

        # ------------------------------------------------------------------

        # Make a grid of model types and select the one with minimum aicc
        not_all_values_gt_zero = not np.all(series_values > 0.0)

        # According to Hyndman (the author of fpp3: Forecatsting: Principles and Practice),
        # multiplicative trend models lead to poor forecast and are not considered.
        # The statsmodels Exponential Smoothing (Holt Winters for now) implementation follows Hyndman's book,
        # so the multiplicative trend models are also not included in the model selection.
        trend_grid = ["A", "N"]

        # holtwinters implementation in statsmodels requires seasonality > 1 for seasonal models,
        # so we enforce it here.
        if self.seasonality > 1:
            seasonal_grid = ["A", "M", "N"]
        else:
            seasonal_grid = ["N"]
        damped_grid = [True, False]
        type_grid = product(trend_grid, seasonal_grid, damped_grid)
        fit_models = {mtype: fit_sm(mtype) for mtype in type_grid if model_is_valid(mtype, not_all_values_gt_zero)}
        fit_models = {mtype: model for mtype, model in fit_models.items() if model is not None}
        if len(fit_models) == 0:
            raise exceptions.FitException._with_error(
                AzureMLError.create(
                    ForecastingExpoSmoothingNoModel,
                    reference_code=ReferenceCodes._FORECASTING_MODELS_EXPOSMOOTHING_NO_MODEL,
                    time_series_grain_id=grain_level
                )
            )

        best_type, model = min(fit_models.items(), key=lambda it: getattr(it[1], "aicc", float("inf")))

        return model

    def _fit_single_grain_impl(self, X_pred_grain: TimeSeriesDataSet, grain_level: GrainType) -> Any:
        """
        Train the Exponential Smoothing model on one grain.

        :param X_pred_grain: The data frame with one grain.
        :type X_pred_grain: TimeSeriesDataSet
        :param grain_level: The name of a grain.
        :type: grain_level: GrainType
        :returns: The Exponential smoothing model.
        :type: Any.

        """
        return self._model_selection_exponential_smoothing(X_pred_grain.data, grain_level)

    def _extend_single_series_impl(self, tsds_context: TimeSeriesDataSet, series_id: GrainType) -> Any:
        """Extend the model for series ID on the given context."""
        Contract.assert_true(series_id in self._models, 'Model not found for the given series id', log_safe=True)
        Contract.assert_type(self._models[series_id], 'self._models[series_id]',
                             holtwinters.results.HoltWintersResultsWrapper)
        # holtwinters doesn't have an API for extension, so simply create a new model with the same parameters
        # but with the context appended to the training series.
        # This is inefficient, but it works and doesn't rely on too many statsmodels internals
        model_obj: holtwinters.results.HoltWintersResults = self._models[series_id]
        y_new_context = tsds_context.data[tsds_context.target_column_name].to_numpy()
        try:
            sm_mod_results = model_obj._results
            sm_mod_params = sm_mod_results.params
            sm_mod = sm_mod_results.model
            y_context = np.append(sm_mod.endog, y_new_context)
            extended_mod = holtwinters.ExponentialSmoothing(y_context, trend=sm_mod.trend, seasonal=sm_mod.seasonal,
                                                            seasonal_periods=sm_mod.seasonal_periods,
                                                            damped_trend=sm_mod.damped_trend,
                                                            initialization_method=None,
                                                            )
            extended_results = extended_mod._predict(h=0, **sm_mod_params)
        except Exception as e:
            msg = f'Encountered an exception of type {type(e).__name__} ' + \
                'while trying to extend ExponentialSmoothing model.'
            raise exceptions.ClientException._with_error(
                AzureMLError.create(
                    AutoMLInternalLogSafe, error_message=msg,
                    error_details=str(e),
                    inner_exception=e
                )
            )
        return extended_results
