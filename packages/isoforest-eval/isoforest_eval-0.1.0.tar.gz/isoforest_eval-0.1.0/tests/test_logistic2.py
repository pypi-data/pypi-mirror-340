from sklearn.datasets import load_breast_cancer
import pandas as pd
import numpy as np
from isoforest_eval import run_isolation_forest

data = load_breast_cancer()
cancer_df = pd.DataFrame(data.data, columns=data.feature_names)
cancer_df['target'] = data.target

# Cancer cleaning
# Quality Control: Handling missing values (if any)
cancer_df = cancer_df.dropna()

# Quality Control: Removing highly correlated features
correlation_matrix = cancer_df.corr().abs()
upper_tri = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
# Find features with high correlation (threshold = 0.9)
to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.9)]
cancer_df = cancer_df.drop(columns=to_drop)

columns_to_remove = ['symmetry error', 'fractal dimension error', 'texture error', 
                     'smoothness error', 'mean fractal dimension']

cancer_df.drop(columns=columns_to_remove, inplace=True, errors='ignore')


cancer_target_column = "target"
contamination_levels = ['auto']
param_grid = {
    "n_estimators": [200],
    "max_samples": ['auto'],
    "contamination": contamination_levels,
    "max_features": [1.0],
    "random_state": [42]
}

results = run_isolation_forest(cancer_df, cancer_target_column, param_grid, model_type="auto")
results.sort_values(by="Log Loss", ascending=False).head(5)
print(results)
results.to_csv("isoforest_logistic_results.csv", index=False)