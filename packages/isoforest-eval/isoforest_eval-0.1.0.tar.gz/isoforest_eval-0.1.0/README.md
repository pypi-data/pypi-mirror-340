# IsoForest Eval

A Python library to evaluate **Isolation Forest** anomaly detection using either **linear** or **logistic regression** to tune
the hyperparameters of the unsupervised learning algorithm.

## Features

- Split and standardize datasets
- Evaluate linear regression (RMSE, R², MNND)
- Evaluate logistic regression (Accuracy, Log Loss, AUC, F1, etc.)
- Automatically choose regression type
- Grid search across Isolation Forest hyperparameters

## Installation

From local:

```bash
pip install -e .
