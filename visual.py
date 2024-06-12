import pandas as pd
import streamlit as st
from io import BytesIO
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# Upload Excel file
inputExcelFile = st.sidebar.file_uploader("Upload Excel File", type=["xlsx", "xls"])

if inputExcelFile is not None:
    # Read the uploaded Excel file
    df = pd.read_excel(inputExcelFile)
    st.write(df.columns)
       # Extract the month and year from 'order_date' to create a new column 'order_month'
    df['month'] = pd.DatetimeIndex(df['order_date']).month
    grouped_df = df.groupby(['month', 'party_name'])['total_value'].sum().reset_index()

    #grouped_df = df.groupby('month').size().reset_index(name='Count')

    st.write("### Grouped DataFrame by Month")
    st.dataframe(grouped_df)

# Prepare data for ECharts
months = grouped_df['month'].unique()
parties = grouped_df['party_name'].unique()

line = Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))

line.add_xaxis(list(months))

for party in parties:
    party_data = grouped_df[grouped_df['party_name'] == party]
    values = [party_data[party_data['month'] == month]['total_value'].sum() for month in months]
    line.add_yaxis(party, values, is_smooth=True)

line.set_global_opts(
    title_opts=opts.TitleOpts(title="Monthly Total Value by Party Name"),
    xaxis_opts=opts.AxisOpts(type_="category", name="Month"),
    yaxis_opts=opts.AxisOpts(type_="value", name="Total Value"),
    datazoom_opts=[opts.DataZoomOpts()]
)

# Animation options
line.set_series_opts(
    label_opts=opts.LabelOpts(is_show=False),
    markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max", name="Max")]),
    markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="Average")]),
)

# Render the chart
line.render_notebook()
