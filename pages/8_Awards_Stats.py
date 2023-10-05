import streamlit as st
from Connection import *
import pandas as pd
import matplotlib.pyplot as plt
conn, cur = Connection.createConnection()

st.header("Awards Stats")
st.markdown("<br>",unsafe_allow_html=True)

st.subheader("Awards VS Movies plot")
Count = pd.read_sql("Select awards, count(*) as count from movies group by awards",con=conn).dropna()
Plot = Count.plot.bar(x='awards', y='count')
st.pyplot(plt.gcf())
st.write("Select awards,count(*) as count from movies group by awards")

Connection.deleteConnection(conn,cur)