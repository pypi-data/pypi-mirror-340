# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Generic bag of words transformer."""
import logging
from typing import Optional, Tuple, Union

import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline, make_pipeline, make_union
from sklearn.preprocessing import RobustScaler

from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.constants import SupportedTransformersInternal as _SupportedTransformersInternal
from ..._types import CoreDataInputType, CoreDataSingleColumnInputType
from .._azureml_transformer import AzureMLTransformer
from .stats_transformer import StatsTransformer

_logger = logging.getLogger(__name__)


class TFIDF_VECTORIZER_CONFIG:
    """Param values for TFIDF Vectorizer."""

    USE_IDF = False
    NORM = "l2"
    MAX_DF = 0.95
    CHAR_ANALYZER = "char"
    CHAR_NGRAM_RANGE = (3, 3)
    WORD_ANALYZER = "word"
    WORD_NGRAM_RANGE = (1, 2)
    SUBSAMPLE_SIZE = 10000
    MIN_WORD_NGRAM = 2


class BagOfWordsTransformer(AzureMLTransformer):
    """Generic bag of words transformer."""

    def __init__(
        self,
        max_wordgrams: int = int(2e5),
        wordgram_range: Tuple[int, int] = (1, 2),
        chargram_range: Tuple[int, int] = (3, 3),
        norm: str = "l2",
        max_df: float = 1.0,
        include_dense_features: bool = False,
        use_idf: bool = False,
    ) -> None:
        """Create the bag of words transformer."""
        super().__init__()
        self._max_wordgrams = max_wordgrams
        self._wordgram_range = wordgram_range
        self._chargram_range = chargram_range
        self._include_dense_features = include_dense_features
        self._norm = norm
        self._max_df = max_df
        self._pipelines = None  # type: Optional[Union[Pipeline, FeatureUnion]]
        self._use_idf = use_idf
        self._transformer_name = _SupportedTransformersInternal.BagOfWordsTransformer

    def get_params(self, deep=True):
        return {
            "max_wordgrams": self._max_wordgrams,
            "wordgram_range": self._wordgram_range,
            "chargram_range": self._chargram_range,
            "norm": self._norm,
            "max_df": self._max_df,
            "include_dense_features": self._include_dense_features,
            "use_idf": self._use_idf,
        }

    def _get_transformer_name(self) -> str:
        return self._transformer_name

    def _to_dict(self):
        """
        Create dict from transformer for  serialization usage.

        :return: a dictionary
        """
        dct = super(BagOfWordsTransformer, self)._to_dict()
        dct["id"] = "bow_transformer"
        dct["type"] = "text"
        dct["kwargs"]["max_wordgrams"] = self._max_wordgrams
        dct["kwargs"]["wordgram_range"] = list(self._wordgram_range)
        dct["kwargs"]["chargram_range"] = list(self._chargram_range)
        dct["kwargs"]["norm"] = self._norm
        dct["kwargs"]["max_df"] = self._max_df
        dct["kwargs"]["include_dense_features"] = self._include_dense_features
        dct["kwargs"]["use_idf"] = self._use_idf

        return dct

    @function_debug_log_wrapped()
    def fit(self, X: CoreDataInputType, y: CoreDataSingleColumnInputType) -> "BagOfWordsTransformer":
        """
        Fit the current model to given input data.

        :param X: Input data.
        :param y: Input labels.
        :return: The object itself.
        """
        pipeline_list = []
        if self._include_dense_features:
            pipeline_list.append(
                make_pipeline(StatsTransformer(), DictVectorizer(), RobustScaler(with_centering=False))
            )

        # Check to see if chargram can be applied based on max len of text column. If the max len of text
        # in the data is less than the min len required for chargram usage, we don't apply chargram featurizer
        max_len_text = len(max(np.array(X), key=len))
        _logger.info("N-gram length in text col: {}".format(max_len_text))
        if max_len_text < min(self._chargram_range):
            self._chargram_range = (0, 0)
        if self._chargram_range != (0, 0):
            pipeline_list.append(
                TfidfVectorizer(
                    use_idf=self._use_idf,
                    dtype=np.float32,
                    analyzer=TFIDF_VECTORIZER_CONFIG.CHAR_ANALYZER,
                    norm=self._norm,
                    max_df=self._max_df,
                    ngram_range=self._chargram_range,
                )
            )
            _logger.info("Char-gram based features will be added.")

        if max_len_text < TFIDF_VECTORIZER_CONFIG.MIN_WORD_NGRAM:
            self._wordgram_range = (0, 0)
        if self._wordgram_range != (0, 0):
            pipeline_list.append(
                TfidfVectorizer(
                    use_idf=self._use_idf,
                    dtype=np.float32,
                    max_features=self._max_wordgrams,
                    analyzer=TFIDF_VECTORIZER_CONFIG.WORD_ANALYZER,
                    ngram_range=self._wordgram_range,
                )
            )
            _logger.info("Word-gram based features will be added.")

        if pipeline_list:
            self._pipelines = make_union(*pipeline_list)
            self._pipelines.fit(X)
        return self

    @function_debug_log_wrapped()
    def transform(self, X: CoreDataInputType) -> CoreDataInputType:
        """Transform the given data.

        :param X: Input data.
        :return: Transformed data.
        """
        if self._pipelines:
            features = self._pipelines.transform(X)
            return features
        else:
            return np.array([])

    def get_memory_footprint(self, X: CoreDataInputType, y: CoreDataSingleColumnInputType) -> int:
        # We will revisit this later.
        return 0
