import streamlit as st
from Connection import *
import pandas as pd
import matplotlib.pyplot as plt

conn, cur = Connection.createConnection()

st.header("Geography Stats")
st.markdown("<br>",unsafe_allow_html=True)

st.subheader("Geography VS Studios plot")
studioCount = pd.read_sql("Select country,count(*) as count from studios group by country",con=conn).dropna()
studioPlot = studioCount.plot.bar(x='country', y='count')
st.pyplot(plt.gcf())
st.write("Select country,count(*) as count from studios group by country")

st.subheader("Geography VS Actors plot")
ActorsCount = pd.read_sql("Select country, count(*) as count from actors group by country",con=conn).dropna()
actorsPlot = ActorsCount.plot.bar(x='country', y='count')
st.pyplot(plt.gcf())
st.write("Select country, count(*) as count from actors group by country")

st.subheader("Geography VS Awards plot")
AwardsCount = pd.read_sql("SELECT country, count(*) as count from awardstype group by country",con=conn).dropna()
awardsPlot = AwardsCount.plot.bar(x='country', y='count')
st.pyplot(plt.gcf())
st.write("SELECT country, count(*) as count from awardstype group by country")
Connection.deleteConnection(conn,cur)