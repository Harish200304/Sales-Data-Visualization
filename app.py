import streamlit as st
from preprocessor import load_data, preprocess_data
from helper import (
    get_num_columns,
    get_cat_columns,
    date_columns,
    sales_summary,
    plot_pie_chart,
    plot_sales_by_category,
    plot_top_items
)

st.set_page_config(page_title="Sales Data Analysis", layout="wide")

st.title("Sales Data Analysis Dashboard")

uploaded_file = st.file_uploader(
    "Upload your sales data file",
      type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    df = preprocess_data(uploaded_file)
    
    st.subheader("Preview:")
    st.dataframe(df.head())
    
    st.subheader("Summary")

    summary = sales_summary(df)
    cols = st.columns(len(summary))

    for col, (label, value) in zip(cols, summary.items()):
        if isinstance(value, float):
            col.metric(label, f"{value:,.2f}")
        else:
            col.metric(label, f"{value:,}")
        
    num_cols = get_num_columns(df)
    cat_cols = get_cat_columns(df)
    date_cols = date_columns(df)

    st.subheader("Visualizations")
    if date_cols:
        date_col = st.selectbox("Select Date Column", date_cols)
        year_col = f"{date_col}_year"
        df[year_col] = df[date_col].dt.year
        fig = plot_pie_chart(df, year_col)
        st.plotly_chart(fig, use_container_width=True)
    
    if cat_cols:
        category_col = st.selectbox("Select Category Column", cat_cols)
        fig = plot_sales_by_category(df, category_col, 'total_sales')
        st.plotly_chart(fig, use_container_width=True)

        top_n = st.slider("Select Top N Categories", min_value=1, max_value=20, value=10)
        fig = plot_top_items(df, category_col, 'total_sales', top_n)
        st.plotly_chart(fig, use_container_width=True)
