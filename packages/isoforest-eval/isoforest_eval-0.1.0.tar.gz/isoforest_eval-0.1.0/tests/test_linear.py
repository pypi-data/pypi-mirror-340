
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from isoforest_eval import run_isolation_forest

who_df = pd.read_csv("../Data/Life_Expectancy_Data.csv")

# WHO cleaning
# Drop irrelevant columns ('Country' is not useful for regression)
who_df = who_df.drop(columns=['Country'], errors='ignore')

# Rename target column to remove any trailing spaces
who_df = who_df.rename(columns={'Life expectancy ': 'Life_expectancy'})

# Encode categorical variables ('Status' column)
label_encoder = LabelEncoder()
who_df['Status'] = label_encoder.fit_transform(who_df['Status'])

# Handle missing values by imputing the median
who_df = who_df.fillna(who_df.median())

# Remove highly correlated features (Threshold: 0.9)
correlation_matrix = who_df.corr().abs()
upper_tri = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.9)]
who_df = who_df.drop(columns=to_drop)
#print(who_df.head(5))

WHO_target_column = "Life_expectancy"
contamination_levels = [0.001,0.002,0.003,0.004,0.005,.006,0.007,0.008,0.009,0.01, 0.02, 0.05, 0.1,0.2,0.3,0.4]
param_grid = {
    "n_estimators": [100, 200,300, 400, 500],
    "max_samples": [0.8, 0.9],
    "contamination": contamination_levels,
    "max_features": [0.8,0.9,1.0],
    "random_state": [42]
}


results = run_isolation_forest(who_df, WHO_target_column, param_grid, model_type="auto")
results.sort_values(by="RMSE", ascending=True).head(20)

print(results)

results.to_csv("isoforest_linear_results.csv", index=False)