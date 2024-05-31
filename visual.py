import streamlit as st
from streamlit_echarts import st_echarts

# Sample data
data = [
    {"value": 8, "name": 'A'},
    {"value": 7, "name": 'B'},
    {"value": 6, "name": 'C'},
    {"value": 5, "name": 'D'},
    {"value": 4, "name": 'E'},
    {"value": 3, "name": 'F'},
    {"value": 2, "name": 'G'},
    {"value": 1, "name": 'H'}
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

