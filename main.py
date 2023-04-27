import streamlit as st
from snowflake.snowpark import Session
import pandas as pd
st.title('❄ Inventory Manager')

@st.cache_resource
def create_session():
    return Session.builder.configs(st.secrets.snowflake).create()

session = create_session()

@st.cache_data
def load_data(table_name):
    table = session.table(table_name)
    table = table.limit(100)
    table = table.collect()
    return table

table_name = "STOCK.PUBLIC.MYTABLE"

with st.expander("See Table"):
    af = pd.DataFrame(load_data(table_name))
    st.dataframe(af)


df = pd.DataFrame(load_data(table_name))
df.fillna(0, inplace=True)
grouped_data = df.groupby(['PRODUCT_NAME']).sum().reset_index()
st.bar_chart(grouped_data)
