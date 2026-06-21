# ================
# Tạo dữ liệu cần thiết:
# 1/ RFM (Recency - Frequency - Monetary)
# 2/
# 3/
# ================
import pandas as pd
from utils.config import PROCESSED_DATA_DIR

def create_rfm_data(df : pd.DataFrame) -> pd.DataFrame:
    """
    Tạo dữ liệu RFM - Cho phân cụm KMeans, DBSCAN
    Step-by-Step:
    1/ Lọc bỏ các mã khách hàng = 0 và các mã sản phẩm chỉ chứa chữ
    2/ Xác định ngày hiện tại = max(df["InvoiceDate"]) + 1 ngày
    3/ Gộp các CustomerID thành nhóm và tính RFM:
    - R: Số ngày từ lần mua cuối
    - F: Số lần mua hàng
    - M: Tổng chi tiêu
    4/ Thêm cột RFM vào DataFrame gốc
    5/ Lưu dữ liệu vào đường dẫn PROCESSED_DATA_DIR / rfm_data.csv
    """
    df_clean = df.copy()

    df_clean = df_clean[df_clean["CustomerID"] != 0]
    df_clean = df_clean[~df_clean["StockCode"].astype(str).str.contains("^\D*$", regex=True)]
    
    current_date = df_clean["InvoiceDate"].max() + pd.Timedelta(days=1)

    df_rfm = df_clean.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (current_date - x.max()).days,
        "InvoiceNo": "nunique",
        "Total": "sum"
    }).reset_index()

    df_rfm.rename(columns={
        "InvoiceDate": "Recency",
        "InvoiceNo": "Frequency",
        "Total": "Monetary"
    }, inplace=True)

    df_rfm.to_csv(PROCESSED_DATA_DIR / "rfm_data.csv", index=False)
    print("Save file in rfm_data.csv")
    return df_rfm

def create_regression_or_classification_data(df : pd.DataFrame, cut_off_date : str, is_classify : bool = False) -> pd.DataFrame:
    """
    Tạo dữ liệu Regression - Cho dự đoán
    Step-by-Step:
    1/ Lọc bỏ các mã khách hàng = 0 và các mã sản phẩm chỉ chứa chữ
    2/ Chia tập dữ liệu làm 2 phần Train và Test
    3/ Gộp các CustomerID thành nhóm và tạo các biến độc lập:
    - Total_spend : Tổng chi tiêu
    - Frequency : Số đơn mua hàng
    - Total_Items : Tổng sản phẩm đã mua
    - Unique_Products : Số sản phẩm khác nhau (độ đa dạng của khách hàng)
    - Avg_Basket_Value : Giá trị trung bình mỗi đơn (Total_spend/Frequency)
    4/ Tạo biến mục tiêu
    - LTV (Lifetime Value): Nếu tương lai có quay lại mua -> Tổng chi tiêu tương lại
                                        không có          -> 0
    - Churn (Mất khách): Nếu LTV > 0 -> = 0 (khách vẫn quay lại)
                                 = 0 -> = 1 (khách đã rời bỏ)
    5/ Kết hợp 2 bảng dữ liệu quá khứ và tương lai dựa vào CustomerID
    6/ Lưu dữ liệu vào đường dẫn PROCESSED_DATA_DIR / regression_data.csv hoặc classification_data.csv
    """
    df_clean = df.copy()
    
    df_clean = df_clean[df_clean["CustomerID"] != 0]
    df_clean = df_clean[~df_clean["StockCode"].astype(str).str.contains("^\D*$", regex=True)]

    cut_off_date = pd.to_datetime(cut_off_date)

    df_history = df_clean[df_clean["InvoiceDate"] < cut_off_date]
    df_future = df_clean[df_clean["InvoiceDate"] >= cut_off_date]

    features = df_history.groupby("CustomerID").agg({
        "Total" : "sum",
        "InvoiceNo" : "nunique",
        "Quantity" : "sum",
        "StockCode" : "nunique",
    }).reset_index()

    features.rename(columns={
        "Total" : "Total_Spend",
        "InvoiceNo" : "Frequency",
        "Quantity" : "Total_Items",
        "StockCode" : "Unique_Products"
    }, inplace=True)

    features["Avg_Basket_Value"] = features["Total_Spend"] / features["Frequency"]

    target = df_future.groupby("CustomerID").agg({"Total" : "sum"}).reset_index()
    target.rename(columns={"Total" : "LTV"}, inplace=True)

    regression_df = features.merge(target, on="CustomerID", how="left")
    regression_df["LTV"] = regression_df["LTV"].fillna(0)
    
    if is_classify:
        regression_df["Churn"] = (regression_df["LTV"] == 0).astype(int)
        regression_df.drop("LTV", axis=1, inplace=True)
        regression_df.to_csv(PROCESSED_DATA_DIR / "classification_data.csv", index=False)
    else:
        regression_df.to_csv(PROCESSED_DATA_DIR / "regression_data.csv", index=False)
    
    print(f"Save file in {'classification_data.csv' if is_classify else 'regression_data.csv'}")
    return regression_df

def create_timeseries_data(df : pd.DataFrame) -> pd.DataFrame:
    """
    Tạo dữ liệu Time Series - Cho dự đoán doanh thu theo tuần
    1/ Đưa InvoiceDate làm index
    2/ Resample dữ liệu theo 'W' (tuần) và tính tổng doanh thu trong tuần
    3/ Làm gọn tên cột và lưu dữ liệu vào đường dẫn PROCESSED_DATA_DIR / timeseries_data.csv
    """
    df_ts = df.copy()

    df_ts.set_index('InvoiceDate', inplace=True)

    ts_data = df_ts['Total'].resample('W').sum().reset_index()
    ts_data.rename(columns={
        'InvoiceDate' : 'Date',
        'Total' : 'Weekly_Sales'
    }, inplace=True)
    
    ts_data.to_csv(PROCESSED_DATA_DIR / "timeseries_data.csv", index=False)
    print(f"Save file in timeseries_data.csv")
    return ts_data

    