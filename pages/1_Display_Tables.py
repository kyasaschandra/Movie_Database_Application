import streamlit as st
from Connection import *
from st_aggrid import AgGrid
import pandas as pd

conn, cur = Connection.createConnection()
st.title("Display Tables")

tabMovies, tabPeople, tabStudios, tabActors, tabAwards, tabCat, tabProcess, tabGeo, tabCast = st.tabs(["Movies", "People", "Studios", "Actors","Awards", "Categories", "Process", "Geography", "Casts"])

with tabCast:
    st.header("Casts")
    casts = pd.read_sql("SELECT * from casts", con=conn)
    st.write(casts)
    #AgGrid(movies,height=500,width=500)
    
with tabMovies:
    st.header("Movies")
    movies = pd.read_sql("SELECT * from movies", con=conn)
    st.write(movies)
    #AgGrid(movies,height=500,width=500)

with tabPeople:
    st.header("People")
    people = pd.read_sql("SELECT * from people", con=conn)
    st.write(people)
    #AgGrid(people,height=500,width=500)

with tabStudios:
    st.header("Studios")
    studios = pd.read_sql("SELECT * from studios", con=conn)
    st.write(studios)
    #AgGrid(studios,height=500,width=500)

with tabActors:
    st.header("Actors")
    actors = pd.read_sql("SELECT * from actors", con=conn)
    st.write(actors)
    #AgGrid(actors,height=500,width=500)

with tabAwards:
    st.header("Awards")
    awards = pd.read_sql("SELECT * from awardstype", con=conn)
    st.write(awards)
    #AgGrid(awards,height=500,width=500)

with tabCat:
    st.header("Categories")
    categories = pd.read_sql("SELECT * from categories", con=conn)
    st.write(categories)
    #AgGrid(categories,height=500,width=500)

with tabProcess:
    st.header("Process")
    colorcodes = pd.read_sql("SELECT * from colorcodes", con=conn)
    st.write(colorcodes)
    #AgGrid(colorcodes,height=500,width=500)

with tabGeo:
    st.header("Geography")
    geography = pd.read_sql("SELECT * from geography", con=conn)
    st.write(geography)
    #AgGrid(geography,height=500,width=500)



Connection.deleteConnection(conn,cur)