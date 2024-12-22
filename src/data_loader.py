import pandas as pd

def load_csv_data(file_path):
    """
    Loads data from a CSV file.

    Parameters:
        file_path (str): Path to the data CSV file.

    Returns:
        DataFrame: Loaded data.
    """
    return pd.read_csv(file_path)