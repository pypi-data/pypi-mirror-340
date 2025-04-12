# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Base objects for Transformers and Estimators."""
from typing import Any, Dict
from abc import ABCMeta

from sklearn.base import BaseEstimator, TransformerMixin
from azureml.automl.core import _codegen_utilities
from azureml.training.tabular.featurization._azureml_transformer import \
    AzureMLTransformer as AzureMLForecastTransformerBase
from azureml.training.tabular.featurization.timeseries._grain_based_stateful_transformer import \
    _GrainBasedStatefulTransformer


class AzureMLForecastEstimatorBase(BaseEstimator, metaclass=ABCMeta):
    """Base estimator for all AzureMLForecastSDK."""

    def __repr__(self):
        return _codegen_utilities.generate_repr_str(self.__class__, self.get_params(deep=False))

    """
    def fit(self, X, y):
        A reference implementation of a fitting function

        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samples, n_features]
            The training input samples.
        y : array-like, shape = [n_samples] or [n_samples, n_outputs]
            The target values (class labels in classification, real numbers in
            regression).

        Returns
        -------
        self : object
            Returns self.

        X, y = check_X_y(X, y)
        # Return the estimator
        return self


    def predict(self, X):
        A reference implementation of a predicting function.

        Parameters
        ----------
        X : array-like of shape = [n_samples, n_features]
            The input samples.

        Returns
        -------
        y : array of shape = [n_samples]
            Returns :math:`x^2` where :math:`x` is the first column of `X`.
        X = check_array(X)
        return X[:, 0]**2
        pass
    """
