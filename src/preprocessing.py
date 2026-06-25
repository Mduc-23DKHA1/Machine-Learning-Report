import pandas as pd

def overview_data(df : pd.DataFrame) -> None:
    print(f"Kích thước dữ liệu = ({df.shape[0]},{df.shape[1]})")
    print(f"{'='*40}\n\nBảng Kiểu dữ liệu")
    print(df.info())
    print(f"{'='*40}\n\nBảng Phân phối dữ liệu")
    print(df.describe(include='all'))
    print(f"{'='*40}\n\nBảng Mất dữ liệu")
    print(df.isna().sum())
    print(f"{'='*40}\n\nBảng dữ liệu trùng")
    print(df.duplicated().sum())
    print(f"{'='*40}\n\n")

def clean_data(df : pd.DataFrame) -> pd.DataFrame:
    """
    Data Cleaning step-by-step:
    1/ Remove Duplicate
    2/ Remove NaN in Description, Quantity, UnitPrice
    3/ Transform InvoiceDate to datetime
    4/ Remove invalid data
    5/ Fill CustomerID with 0
    6/ Transform features to correct type
    """
    df = df.drop_duplicates()
    df.dropna(
        subset=["Description", "Quantity", "UnitPrice"],
        inplace=True
    )
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"],
        dayfirst=True
    )
    mask = (
        (df["UnitPrice"] > 0)
        & (df["Quantity"] > 0)
        & (~df["InvoiceNo"].astype(str).str.startswith(("A", "C"), na=False))
    )
    df = df[mask]
    df["CustomerID"] = df["CustomerID"].fillna(0)

    df["InvoiceNo"] = df["InvoiceNo"].astype(int)
    df["Description"] = df["Description"].astype(str)
    df["CustomerID"] = df["CustomerID"].astype(int)

    return df

def feature_engineering(df : pd.DataFrame) -> pd.DataFrame:
    """
    Feature Engineering step-by-step:
    1/ TotalOrder = Quantity * UnitPrice
    2/ Day, Month, Year, DayOfWeek, Hour, Quarter, Weekday
    """
    df["Total"] = df["Quantity"] * df["UnitPrice"]

    df["Day"] = df["InvoiceDate"].dt.day
    df["Month"] = df["InvoiceDate"].dt.month
    df["Year"] = df["InvoiceDate"].dt.year
    df["DayOfWeek"] = df["InvoiceDate"].dt.dayofweek

    df["Hour"] = df["InvoiceDate"].dt.hour
    df["Quarter"] = df["InvoiceDate"].dt.quarter
    df["Weekday"] = df["InvoiceDate"].dt.day_name()

    return df    
