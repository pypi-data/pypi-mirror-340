# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Transformer that concatenates two more columns into a single column."""
from typing import Optional

import numpy as np

from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from ..._types import CoreDataInputType, CoreDataSingleColumnInputType
from .. import _memory_utilities
from .._azureml_transformer import AzureMLTransformer


class StringConcatTransformer(AzureMLTransformer):
    """Transformer that concatenates two more columns into a single column."""

    def __init__(self, separator: str = ". "):
        """Construct string concat transformer.

        :param separator: Separator to insert between columns.
        """
        super().__init__()
        self._separator = separator

    def get_params(self, deep=True):
        return {"separator": self._separator}

    @function_debug_log_wrapped()
    def fit(
        self, X: CoreDataInputType, y: Optional[CoreDataSingleColumnInputType] = None
    ) -> "StringConcatTransformer":
        """
        The fit method.

        :param X: The data to transform.
        :param y: Target values.
        :return: The instance object: self.
        """
        return self

    @function_debug_log_wrapped()
    def transform(self, X: Optional[CoreDataInputType]) -> Optional[CoreDataSingleColumnInputType]:
        """
        Transform data x.

        :param X: The data to transform.
        :type X: numpy.ndarray or pandas.core.series.Series
        :return: Single column with concatenated values in each row.
        """
        if X is None or len(X) == 0:
            return None

        output = []
        # Handle row iteration for numpy arrays or dataframes
        is_arr = isinstance(X, np.ndarray)
        if is_arr:
            iterable = X
        else:
            iterable = X.itertuples()
        for row in iterable:
            if not is_arr:
                row = row[1:]
            output.append(self._separator.join(row))
        return np.array(output)

    def get_memory_footprint(self, X: CoreDataInputType, y: CoreDataSingleColumnInputType) -> int:
        """
        Obtain memory footprint estimate for this transformer.

        :param X: Input data.
        :param y: Input label.
        :return: Amount of memory taken.
        """
        num_rows = len(X)
        f_size = _memory_utilities.get_data_memory_size(str)
        return num_rows * f_size
