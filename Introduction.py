import streamlit as st
def display(conn, cur):

    count = 0
    cur.execute("Select count(*) from movies")
    count = cur.fetchall()
    #print(count)
    st.title("DMQL Project: Movies Database")
    st.markdown("<br>",unsafe_allow_html=True)
    count = "<h1 style='text-align: center; color: grey;'>"+str(count[0][0])+"</h1>"
    st.markdown(count, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Movies in Database<h2>",unsafe_allow_html=True)
    cur.execute("Select count(*) from people")
    count = cur.fetchall()
    #print(count)
    st.markdown("<br>",unsafe_allow_html=True)
    count = "<h1 style='text-align: center; color: grey;'>"+str(count[0][0])+"</h1>"
    st.markdown(count, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>People in Database<h2>",unsafe_allow_html=True)
    cur.execute("Select count(*) from studios")
    count = cur.fetchall()
    #print(count)
    st.markdown("<br>",unsafe_allow_html=True)
    count = "<h1 style='text-align: center; color: grey;'>"+str(count[0][0])+"</h1>"
    st.markdown(count, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Studios in Database<h2>",unsafe_allow_html=True)
    cur.execute("Select count(*) from actors")
    count = cur.fetchall()
    #print(count)
    st.markdown("<br>",unsafe_allow_html=True)
    count = "<h1 style='text-align: center; color: grey;'>"+str(count[0][0])+"</h1>"
    st.markdown(count, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Actors in Database<h2>",unsafe_allow_html=True)
    cur.execute("Select count(*) from casts")
    count = cur.fetchall()
    #print(count)
    st.markdown("<br>",unsafe_allow_html=True)
    count = "<h1 style='text-align: center; color: grey;'>"+str(count[0][0])+"</h1>"
    st.markdown(count, unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: white;'>Casts in Database<h2>",unsafe_allow_html=True)

from Connection import Connection
conn,cur = Connection.createConnection()
cur.execute("select * from geography")
sample = cur.fetchall()
if len(sample)>0:
    display(conn,cur)
    Connection.deleteConnection(conn,cur)
else:
    Connection.insert()