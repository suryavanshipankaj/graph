import streamlit as st
from streamlit_echarts import st_echarts

# Sample data
data = [
    {"value": 8, "name": 'HR'},
    {"value": 7, "name": 'Accounts'},
    {"value": 6, "name": 'Inventory'},
    {"value": 5, "name": 'Production'},
    {"value": 4, "name": 'Supply chain'},
    {"value": 3, "name": 'IT'},
    {"value": 2, "name": 'DMSD'},
    {"value": 1, "name": 'IBSD'}
]

option = {
    "title": {
        "text": 'Nightingale Rose Chart',
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
            "name": 'Categories',
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

st.title("Nightingale (Rose) Chart Example")

# Display chart in Streamlit
st_echarts(options=option, height="500px")
