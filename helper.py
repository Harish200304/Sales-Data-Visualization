import numpy as np
import pandas as pd
import plotly.express as px

def get_num_columns(df):
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    return num_cols

def get_cat_columns(df):
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    return cat_cols

def date_columns(df):
    date_cols = df.select_dtypes(include=['datetime', 'datetime64']).columns.tolist()
    return date_cols

def sales_summary(df):
    summary = {}

    if 'total_sales' in df.columns:
        summary['total_sales'] = df['total_sales'].sum()
        summary['average_sales'] = df['total_sales'].mean()
        summary['max_sales'] = df['total_sales'].max()
        summary['min_sales'] = df['total_sales'].min()
    summary['num_records'] = len(df)

    return summary

def plot_pie_chart(df, category_col):
    category_counts = df[category_col].value_counts().reset_index()
    category_counts.columns = [category_col, 'count']

    return px.pie(
        category_counts,
        names=category_col,
        values='count',
        title=f'Distribution of {category_col}',
        hole=0.4
    )

def plot_sales_by_category(df, category_col, sales_col):
    category_sales = (
        df.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    return px.bar(
        category_sales,
        x=category_col,
        y=sales_col,
        title='Sales by Category',
        text_auto=True
    )

def plot_top_items(df, category_col, sales_col, top_n=10):
    top_items = (
        df.groupby(category_col)[sales_col]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )

    return px.bar(
        top_items,
        x=category_col,
        y=sales_col,
        title=f'Top {top_n} {category_col} by Sales',
        text_auto=True
    )
