import numpy as np
import pandas as pd
def load_data(file_path):
    filename = getattr(file_path, 'name', str(file_path))

    if filename.endswith('.csv'):
        df = pd.read_csv(file_path, encoding='cp1252')
    elif filename.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")

    return df

def clean_col_names(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(' ', '_')
    )
    return df
def detect_date_cols(df):
    for col in df.columns:
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def create_sales_cols(df):
    if "total_sales" in df.columns:
        return df
    if "sales" in df.columns:
        df["total_sales"] = df["sales"]
    elif "revenue" in df.columns:
        df["total_sales"] = df["revenue"]
    elif "quantity" in df.columns and "price" in df.columns:
        df["total_sales"] = df["quantity"] * df["price"]
    elif "quantity" in df.columns and "unit_price" in df.columns:
        df["total_sales"] = df["quantity"] * df["unit_price"]
    return df

def preprocess_data(data):
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        df = load_data(data)

    df = clean_col_names(df)
    df = detect_date_cols(df)
    df = create_sales_cols(df)
    df = df.drop_duplicates()

    return df
