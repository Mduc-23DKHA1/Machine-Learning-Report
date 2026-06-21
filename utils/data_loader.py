import pandas as pd
from .config import RAW_DATA_DIR, PROCESSED_DATA_DIR


def load_retail_data():
    path = RAW_DATA_DIR / "Online Retail.xlsx"

    return pd.read_excel(path)

def load_rfm_data():
    path = PROCESSED_DATA_DIR / "rfm_data.csv"

    return pd.read_csv(path)

def load_regression_data():
    path = PROCESSED_DATA_DIR / "regression_data.csv"

    return pd.read_csv(path)

def load_classification_data():
    path = PROCESSED_DATA_DIR / "classification_data.csv"

    return pd.read_csv(path)

def load_timeseries_data():
    path = PROCESSED_DATA_DIR / "timeseries_data.csv"

    return pd.read_csv(path)
