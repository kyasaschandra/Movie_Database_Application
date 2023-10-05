import streamlit as st
from Connection import *
import pandas as pd
import matplotlib.pyplot as plt

conn, cur = Connection.createConnection()

st.header("category Stats")
st.markdown("<br>",unsafe_allow_html=True)

st.subheader("Category VS Movies plot")
Count = pd.read_sql("Select category, count(*) as count from movies group by category",con=conn).dropna()
Plot = Count.plot.bar(x='category', y='count')
st.pyplot(plt.gcf())
st.write("Select category,count(*) as count from movies group by category")

Connection.deleteConnection(conn,cur)