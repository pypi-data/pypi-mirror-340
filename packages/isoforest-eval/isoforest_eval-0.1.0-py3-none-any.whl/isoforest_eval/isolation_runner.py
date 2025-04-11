import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import ParameterGrid

from .preprocessing import split_and_standardize_data
from .evaluation import evaluate_linear_regression, evaluate_logistic_regression

def run_isolation_forest(df, target_column, param_grid, model_type="auto", test_size=0.15, random_state=42):
    """
    Runs Isolation Forest, filters inliers, and evaluates performance using specified model.

    Args:
        df (pd.DataFrame): Input dataframe.
        target_column (str): Name of the target variable.
        param_grid (dict): Dictionary of Isolation Forest hyperparameters to grid search.
        model_type (str): 'linear', 'logistic', or 'auto' (default).
        test_size (float): Fraction of data for testing.
        random_state (int): Seed for reproducibility.

    Returns:
        pd.DataFrame: Performance metrics for each parameter configuration.
    """
    x_train, x_test, y_train, y_test = split_and_standardize_data(df, target_column, test_size, random_state)

    if model_type == "auto":
        model_type = "logistic" if y_train.ndim == 1 and len(np.unique(y_train)) <= 2 else "linear"

    results = []

    for params in ParameterGrid(param_grid):
        iforest = IsolationForest(**params)
        labels = iforest.fit_predict(x_train)

        inliers = x_train[labels == 1]
        y_inliers = y_train[labels == 1]

        if model_type == "linear":
            metrics = evaluate_linear_regression(inliers, y_inliers, x_test, y_test)
        elif model_type == "logistic":
            metrics = evaluate_logistic_regression(inliers, y_inliers, x_test, y_test)
        else:
            raise ValueError("Invalid model_type. Choose 'linear' or 'logistic'.")

        metrics.update(params)
        results.append(metrics)

    return pd.DataFrame(results)
