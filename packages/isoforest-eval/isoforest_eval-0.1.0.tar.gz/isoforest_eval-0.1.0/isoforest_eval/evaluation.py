import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error, r2_score, accuracy_score, log_loss,
    precision_score, recall_score, f1_score, roc_auc_score
)
from scipy.spatial.distance import pdist, squareform

def evaluate_linear_regression(x_train, y_train, x_test, y_test):
    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    pairwise_distances = squareform(pdist(x_train))
    np.fill_diagonal(pairwise_distances, np.inf)
    mnnd = np.mean(np.min(pairwise_distances, axis=1))

    return {"RMSE": rmse, "R²": r2, "Mean Nearest Neighbor Distance (MNND)": mnnd}


def evaluate_logistic_regression(x_train, y_train, x_test, y_test):
    model = LogisticRegression(max_iter=10000)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    y_prob = model.predict_proba(x_test)[:, 1]

    return {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Log Loss": log_loss(y_test, y_prob),
        "Precision": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred, zero_division=0),
        "F1-Score": f1_score(y_test, y_pred, zero_division=0),
        "ROC AUC": roc_auc_score(y_test, y_prob),
    }
