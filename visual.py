import pandas as pd
import streamlit as st
from io import BytesIO
from streamlit_echarts import st_echarts

st.title("Generate SQL Script from Excel File")

# Upload Excel file
inputExcelFile = st.sidebar.file_uploader("Upload Excel File", type=["xlsx", "xls"])

if inputExcelFile is not None:
    # Read the uploaded Excel file
    df = pd.read_excel(inputExcelFile)

    # Display the DataFrame
    st.write("### Uploaded DataFrame")
    st.dataframe(df)

    # Calculate missing values and their count column-wise
    missing_values = df.isnull().sum()

    # Create a DataFrame for missing values
    missing_values_df = pd.DataFrame({
        "Column": missing_values.index,
        "Missing Values Count": missing_values.values
    })

    # Display missing values count
    st.write("### Missing Values Count")
    st.dataframe(missing_values_df)

    # Create Nightingale (Rose) Chart for missing values
    data = [{"value": count, "name": col} for col, count in zip(missing_values_df["Column"], missing_values_df["Missing Values Count"])]
    option = {
        "title": {
            "text": 'Missing Values Count',
            "left": 'center'
        },
        "tooltip": {
            "trigger": 'item',
            "formatter": '{a} <br/>{b}: {c} ({d}%)'
        },
        "legend": {
            "top": 'bottom',
            "left": 'center',
            "data": [d["name"] for d in data]
        },
        "series": [
            {
                "name": 'Columns',
                "type": 'pie',
                "radius": [30, 110],
                "center": ['50%', '50%'],
                "roseType": 'area',
                "itemStyle": {
                    "borderRadius": 8
                },
                "data": data
            }
        ]
    }

    st.write("### Nightingale (Rose) Chart for Missing Values")
    st_echarts(options=option, height="500px")

    # Map pandas dtypes to MySQL data types
    dtype_mapping = {
        'object': 'VARCHAR(255)',
        'int64': 'INT',
        'float64': 'FLOAT',
        'datetime64[ns]': 'DATETIME',
        'bool': 'BOOLEAN'
    }

    # Generate the CREATE TABLE statement
    table_name = "table_name"
    columns_with_types = []
    for column, dtype in zip(df.columns, df.dtypes):
        sql_type = dtype_mapping.get(str(dtype), 'VARCHAR(255)')
        columns_with_types.append(f"{column} {sql_type}")
    create_table_statement = f"CREATE TABLE {table_name} (\n" + ",\n".join(columns_with_types) + "\n);"

    # Generate the INSERT INTO statement
    columns = ', '.join(df.columns)
    values_list = []
    for _, row in df.iterrows():
        values = ', '.join([f"'{value}'" if pd.notnull(value) else 'NULL' for value in row.values])
        values_list.append(f"({values})")
    values_str = ',\n'.join(values_list)
    insert_statement = f"INSERT INTO {table_name} ({columns}) VALUES\n{values_str};"

    # Combine both statements
    sql_script = create_table_statement + "\n\n" + insert_statement

    # Display the generated SQL script
    st.write("### Generated SQL Script")
    st.code(sql_script)

    # Function to convert SQL content to a downloadable file
    def create_download_link(sql_content):
        b = BytesIO()
        b.write(sql_content.encode())
        b.seek(0)
        return b

    # Create a downloadable link for the SQL file
    b = create_download_link(sql_script)
    st.download_button(
        label="Download SQL File",
        data=b,
        file_name="script.sql",
        mime="text/sql"
    )
