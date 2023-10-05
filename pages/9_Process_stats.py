import streamlit as st
from Connection import *
import pandas as pd
import matplotlib.pyplot as plt

conn, cur = Connection.createConnection()

st.header("Process Stats")
st.markdown("<br>",unsafe_allow_html=True)

st.subheader("Process VS Movies plot")
Count = pd.read_sql("Select process,count(*) as count from movies group by process",con=conn).dropna()
Plot = Count.plot.bar(x='process', y='count')
st.pyplot(plt.gcf())
st.write("Select process,count(*) as count from movies group by process")

Connection.deleteConnection(conn,cur)