# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""The helper methods to get the columns of specific types."""
import logging
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, cast

import numpy as np
import pandas as pd

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.configuration.feature_config import FeatureConfig
from azureml.automl.core.constants import FeatureType
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    PandasDatetimeConversion,
    TimeseriesDfMissingColumn,
    TimeseriesDfWrongTypeOfGrainColumn)
from azureml.automl.core.shared.constants import TimeSeries
from azureml.automl.core.shared.exceptions import DataException
from azureml.automl.core.shared.forecasting_exception import ForecastingDataException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.core.shared.utilities import \
    _check_if_column_data_type_is_numerical,\
    _check_if_column_data_type_is_datetime
from ..featurization._raw_feature_stats import RawFeatureStats

logger = logging.getLogger(__name__)


def _get_special_columns(time_column_name: str, grain_column_names: Optional[List[str]]) -> Set[str]:
    """
    Return the set of special columns.

    :param time_column_name: The date time column name.
    :param grain_column_names: the optional parameter of grain column names.
    :return: The set of special columns.
    """
    special_columns = {time_column_name}
    if grain_column_names is not None:
        for grain in grain_column_names:
            special_columns.add(grain)
    return special_columns


def get_numeric_columns(
    X: pd.DataFrame,
    time_column_name: str,
    grain_column_names: Optional[List[str]],
    featurization_config: Optional[Union[str, FeaturizationConfig]],
) -> Set[Any]:
    """
    The utility function to get the set of numeric and non-numeric columns in X.

    :param X: The data frame to be analyzed for padding.
    :param time_column_name: The date time column name.
    :param grain_column_names: the optional parameter of grain column names.
    :return: The set of numeric columns.
    """
    return _get_columns_of_type(
        X,
        time_column_name,
        grain_column_names,
        featurization_config,
        FeatureType.Numeric,
        _check_if_column_data_type_is_numerical,
    )


def get_datetime_columns(
    X: pd.DataFrame,
    time_column_name: str,
    grain_column_names: Optional[List[str]],
    featurization_config: Optional[Union[str, FeaturizationConfig]],
) -> Set[Any]:
    """
    The utility function to get the set of datetime columns in X.

    :param X: The data frame to be analyzed for padding.
    :param time_column_name: The date time column name.
    :param grain_column_names: the optional parameter of grain column names.
    :return: The set of datetime columns.
    """
    return _get_columns_of_type(
        X,
        time_column_name,
        grain_column_names,
        featurization_config,
        FeatureType.DateTime,
        _check_if_column_data_type_is_datetime,
    )


def get_drop_columns(
    X: pd.DataFrame,
    timeseries_param_dict: Optional[Dict[str, Any]],
    featurization_config: Optional[FeaturizationConfig] = None
) -> Set[str]:
    """
    The utility function to get the drop columns from training data, X.

    :param X: Input training data.
    :param timeseries_param_dict: The parameters specific to time series.
    :param featurization_config: Featurization configuration if provided by the user.
    :return: The list of to be dropped columns.
    """

    drop_column_names = set()  # type: Set[Any]
    if timeseries_param_dict is not None:
        ts_drop_colum_names = timeseries_param_dict.get(TimeSeries.DROP_COLUMN_NAMES, [])
        if isinstance(ts_drop_colum_names, str):
            drop_column_names.add(ts_drop_colum_names)
        else:
            drop_column_names.update(ts_drop_colum_names)

    # This check is necessary since featurization_config can be either str or object FeaturizationConfig.
    # Only FeaturizationConfig object can contains drop_columns.
    if isinstance(featurization_config, FeaturizationConfig) and featurization_config.drop_columns:
        drop_column_names.update(featurization_config.drop_columns)

    if hasattr(X, 'columns'):
        drop_column_names.update(filter(lambda c: np.sum(X[c].notnull()) == 0, X.columns))

    return drop_column_names


def _get_columns_of_type(
    X: pd.DataFrame,
    time_column_name: str,
    grain_column_names: Optional[List[str]],
    featurization_config: Optional[Union[str, FeaturizationConfig]],
    column_type: str,
    check_function: Callable[[str], bool],
) -> Set[Any]:
    """
    The utility function to get the set of numeric and non-numeric columns in X.

    :param X: The data frame to be analyzed for padding.
    :param time_column_name: The date time column name.
    :param grain_column_names: the optional parameter of grain column names.
    :param column_type: The column type as defined
                        in :class:`azureml.automl.core.constants import FeatureType`.
    :param check_function: the utility function to check if the given column type is
                           the type of interest.
    :return: The set of columns of given type.
    """
    # First infer the column types and get numeric and other column types.
    # Subtract the special column types as grain and time.
    X = infer_objects_safe(X)
    columns_of_interest = set()
    special_columns = _get_special_columns(time_column_name, grain_column_names)
    for col in X.columns:
        if col in special_columns:
            continue
        col_stats = RawFeatureStats(X[col])
        if check_function(col_stats.column_type):
            columns_of_interest.add(col)

    # Modify the column types according to the featurization config.
    if isinstance(featurization_config, FeaturizationConfig):
        if featurization_config.column_purposes is not None:
            for col, purpose in featurization_config.column_purposes.items():
                if col in X.columns and col not in special_columns and purpose == column_type:
                    columns_of_interest.add(col)
                else:
                    columns_of_interest.discard(col)
    return columns_of_interest


def infer_objects_safe(X: pd.DataFrame) -> pd.DataFrame:
    """
    Try to infer objects in the data frame in a safe way.

    :param X: The data frame to be fixed.
    :return: The same data frame instance with the bad timestamps replaced.
    """
    try:
        X = X.infer_objects()
    except pd.errors.OutOfBoundsDatetime:
        # pandas > 0.23 seems to correctly (tested on 0.24.0) handle these
        # large times, while pandas <= 0.23 seems to raise OutOfBoundsDatetime
        X = convert_bad_timestamps_to_strings(X)
        X = X.infer_objects()
    return X


def convert_bad_timestamps_to_strings(X: pd.DataFrame) -> pd.DataFrame:
    """
    Convert bad time stamps to strings.

    Pandas does not support dates earlier than 1677-09-21 00:12:43.145225 or
    later than 2262-04-11 23:47:16.854775807. Here we replace these timestamps with
    string values.
    :param X: The data frame to be fixed.
    :return: The same data frame instance with the bad timestamps replaced.
    """
    # Note: This is a workaround for the old version of pandas this behavior
    # was fixed in pandas > 0.23 (tested on 0.24.0).
    # This code can be removed/refactored when the support of older pandas
    # versions will be dropped.
    for column in X.columns:
        # if the column can not be converted to the datetime, we will convert ti to string.
        if X[column].dtype == np.object_:
            try:
                pd.to_datetime(X[column])
            except pd.errors.OutOfBoundsDatetime:
                X[column] = X[column].astype("str")
            except BaseException:
                # Just a regular non date time column.
                # not an error.
                pass
    return X


def _convert_col_to_purpose(X: Optional[pd.DataFrame], column: Any, purpose: str) -> Optional[pd.DataFrame]:
    """
    Safely convert the column to the given feature_type.

    **Note:** This method is doing the conversion in place, but returns the data frame for convenience.
    :param X: The data frame to make conversion on.
    :param column: The column to be converted.
    :param purpose: The purpose the column have to be converted to.
    :return: The data frame with converted column of None if X was None.
    """
    if X is None:
        return X
    try:
        if purpose in (FeatureType.Text, FeatureType.Categorical,
                       FeatureType.CategoricalHash, FeatureType.Hashes,
                       FeatureType.Ignore):
            # Q: Why we do not convert values to categorical type if user set
            # Categorical type for grain?
            # A: pd.Categorical is a meta information, which is stored in pd.DataFrame
            # object. It will be fragile solution to track this type when
            # transmission of one data frame through the whole training pipeline is
            # not guaranteed.
            X[column] = X[column].astype("str")
        elif purpose == FeatureType.DateTime:
            X[column] = pd.to_datetime(X[column])
        elif purpose == FeatureType.Numeric:
            X[column] = X[column].astype("float")
    except BaseException as exception:
        logging_utilities.log_traceback(
            exception, logger, is_critical=False, override_error_msg="[Masked as it may contain PII]"
        )
    return X


def convert_check_grain_value_types(
    X_train: pd.DataFrame,
    X_valid: Optional[pd.DataFrame],
    time_series_id_column_names: Optional[Union[str, List[str]]],
    featurization_dict: Union[str, Dict[str, Any]],
    ref_code: str,
) -> Tuple[pd.DataFrame, Optional[pd.DataFrame]]:
    """
    Check that the values denoting time series ids contain values of only one data types.

    :param X_train: The training data set.
    :param X_valid: The validation data set if any.
    :param time_series_id_column_names: The list, containing names of the grain columns.
    :param featurization_dict: The dictionary, representing ForecastingConfig.
    :return: Tuple with X_train and X_valid.
    :raises: ForecastingDataException if at least one grain column
             contains values of different types.
    """
    if time_series_id_column_names:
        if isinstance(featurization_dict, dict):
            featurization_config = FeaturizationConfig()
            featurization_config._from_dict(featurization_dict)
            if featurization_config.column_purposes is not None:
                for col, purpose in featurization_config.column_purposes.items():
                    # convert grain to the given type.
                    if col in time_series_id_column_names and col in X_train.columns:
                        X_train = _convert_col_to_purpose(X_train, col, purpose)
                        X_valid = _convert_col_to_purpose(X_valid, col, purpose)

        # Finally check if all values in grain columns contain values of
        # only one type.
        for grain in time_series_id_column_names:
            if grain not in X_train.columns:
                continue
            g_train = X_train[grain]
            if X_valid is not None:
                g_train = g_train.append(X_valid[grain])
            set_dtypes = {type(val) for val in g_train if val is not None}
            if len(set_dtypes) > 1:
                has_compatible_dtype = False
                if not any(type(dt).__module__.startswith("pandas") for dt in set_dtypes):
                    # Sometimes we may have comparable dtypes, for example,
                    # str and np.str_ or np.int32 and np.int64.
                    if (
                        all(np.issubdtype(dt, np.number) for dt in set_dtypes)
                        or all(np.issubdtype(dt, np.datetime64) for dt in set_dtypes)
                        or all(np.issubdtype(dt, np.str_) for dt in set_dtypes)
                    ):
                        has_compatible_dtype = True
                # The dtypes are different and not compatible, giving up.
                if not has_compatible_dtype:
                    raise ForecastingDataException._with_error(
                        AzureMLError.create(
                            TimeseriesDfWrongTypeOfGrainColumn,
                            target="time_series_id_columns",
                            reference_code=ref_code,
                            column=grain, num_types=len(set_dtypes))
                    )
    return X_train, X_valid


def convert_to_datetime(X: pd.DataFrame, time_column_name: str) -> pd.DataFrame:
    """
    Convert time column to datetime only if it is not in this format already.

    **Note:** This function does not create a copy of data frame.
    :param X: The affected data frame.
    :param time_column_name: The name of a time column name.
    :return: The data frame, for which time_column_name us guaranteed to be a datetime.
    """
    if time_column_name not in X.columns:
        raise ForecastingDataException._with_error(
            AzureMLError.create(TimeseriesDfMissingColumn,
                                target=TimeSeries.TIME_COLUMN_NAME,
                                reference_code=ReferenceCodes._FREQUENCY_FIXER_CONVERT_COLUMN_NOT_FOUND,
                                column_names=time_column_name)
        )
    # If the time column dtype is pd.Categorical np.issubdtype will fail
    # because it is pandas dtype. In this case we can apply pd.to_datetime
    # directly.
    if not isinstance(X[time_column_name].dtype, np.dtype) or not np.issubdtype(
        X[time_column_name].dtype, np.datetime64
    ):
        try:
            X[time_column_name] = pd.to_datetime(X[time_column_name])
        except Exception as e:
            raise DataException._with_error(
                AzureMLError.create(PandasDatetimeConversion, target="X", column=time_column_name,
                                    column_type=X[time_column_name].dtype,
                                    reference_code=ReferenceCodes._FREQUENCY_FIXER_CONVERT_INVALID_VALUE),
                inner_exception=e
            ) from e
    return X
