from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def split_and_standardize_data(df, target_column, test_size=0.15, random_state=42):
    """
    Splits the dataframe into training and test sets and applies standard scaling.

    Args:
        df (pd.DataFrame): Input dataframe.
        target_column (str): Name of the target column.
        test_size (float): Fraction of data to be used for testing.
        random_state (int): Seed for reproducibility.

    Returns:
        Tuple of (x_train, x_test, y_train, y_test)
    """
    X = df.drop(columns=[target_column])
    y = df[target_column]

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    return x_train, x_test, y_train, y_test
