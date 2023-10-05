import streamlit as st
from Connection import *
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

conn, cur = Connection.createConnection()

st.title("Query People Table")

tabQuery, tabAdd, tabUpdate, tabDelete = st.tabs(["Query", "Add", "Update","Delete"])

with tabQuery:
    ref_name = pd.read_sql("SELECT distinct ref_name from people",con=conn)
    d_id = pd.read_sql("SELECT distinct d_id from people",con=conn)
    years = pd.read_sql("SELECT distinct years from people",con=conn)
    last_name = pd.read_sql("SELECT distinct last_name from people",con=conn)
    first_name = pd.read_sql("SELECT distinct first_name from people",con=conn)
    yob = pd.read_sql("SELECT distinct yob from people",con=conn)
    yodeath = pd.read_sql("SELECT distinct yodeath from people",con=conn)
    st.header("Query the People table")
    st.markdown("<br>",unsafe_allow_html=True)

    ref_name = st.multiselect("Select Reference Name", ref_name,[])
    ref_name_d_id = st.selectbox(" ",["AND","OR"])
    d_id = st.multiselect("Select Director's ID",d_id,[])
    d_id_years = st.selectbox("  ",["AND","OR"])
    years = st.multiselect("Select years of work",years,[])
    years_last_name = st.selectbox("       ",["AND","OR"])
    last_name = st.multiselect("Select Last Name",last_name,[])
    last_name_first_name = st.selectbox("   ",["AND","OR"])
    first_name = st.multiselect("Select First Name",first_name,[])
    first_name_yob = st.selectbox("    ",["AND","OR"])
    yob = st.multiselect("Select Year of Birth",yob,[])
    yob_ydeath = st.selectbox("                  ",["AND","OR"])
    yodeath = st.multiselect("Select Year of Death",yodeath,[])

    query = "SELECT * from people"
    if ref_name or first_name or years or yob or yodeath or last_name or d_id:
        query = query+" Where "

    if len(ref_name)> 0:
        query = query +" (" 
        for i in ref_name:
            
            if i is None:
                query = query+ " ref_name is NULL or "
            else:
                query = query + "ref_name = '"+i+"' or "
        query = query[:-3]+") "
        
    if len(d_id)>0:
        if ref_name:
            query = query + ref_name_d_id
        query = query+" ("
        for i in d_id:
            if i is None:
                query = query+ " d_id is NULL or "
            else:
                query = query + "d_id = '"+i+"' or "
        query = query[:-3] +") "
        
    if len(years)>0:
        if ref_name or years:
            query = query + d_id_years
        query = query +" ("
        for i in years:
            if i is None:
                query = query+ " years is NULL or "
            else:
                query = query + " years = '"+i+"' or "
        query=query[:-3]+") "

    if len(last_name)>0:
        if ref_name or years or d_id:
            query = query + years_last_name
        query = query +" ("
        for i in last_name:
            if i is None:
                query = query+ " last_name is NULL or "
            else:
                query = query + " last_name = '"+i+"' or "
        query=query[:-3]+") "
    
    if len(first_name)>0:
        if ref_name or last_name or years or d_id:
            query = query + last_name_first_name
        query = query +" ("
        for i in last_name_first_name:
            if i is None:
                query = query+ " first_name is NULL or "
            else:
                query = query + " first_name = '"+i+"' or "
        query=query[:-3]+") "

    if len(yob)>0:
        if ref_name or last_name or years or first_name or d_id:
            query = query + first_name_yob
        query = query +" ("
        for i in yob:
            if i is None:
                query = query+ " yob is NULL or "
            else:
                query = query + " yob = '"+i+"' or "
        query=query[:-3]+") "
    
    if len(yodeath)>0:
        if ref_name or first_name or years or last_name or yob or d_id:
            query = query + yob_ydeath
        query = query +" ("
        for i in yodeath:
            if i is None:
                query = query+ " yodeath is NULL or "
            else:
                query = query + " yodeath = '"+i+"' or "
        query=query[:-3]+") "

    st.write(query)
    result = pd.read_sql(query,con=conn)
    st.write(result)


with tabAdd:
    st.header("Add People")
    addref_name,addd_id,addyears,addlast_name,addfirst_name,addyob,addyodeath = 'Null', 'NULL', 'NULL','NULL','NULL','NULL','NULL'
    
    addref_name = st.text_input("Enter Reference Name")
    addd_id = st.text_input("Enter Director's ID")
    addyears = st.text_input("Enter Years of work")
    addlast_name = st.text_input("Enter Last Name")
    addfirst_name = st.text_input("Enter First Name")
    addyob = st.text_input("Enter year of Birth")
    addyodeath = st.text_input("Enter year of death")

    query = f"INSERT INTO people (ref_name, codes, d_id, years, last_name, first_name, yob, yodeath,country) values ('{addref_name}','{addd_id}','{addyears}','{addlast_name}','{addfirst_name}','{addyob}','{addyodeath}')"
    st.write(query)
    addPeople = st.button("Add People")
    if addPeople:
        if addd_id or addfirst_name or addlast_name or addref_name or addyears or addyob or addyodeath:
            cur.execute(query)
            conn.commit()
            st.success("People added")
        else:
            st.error("Please check and try again")

with tabUpdate:
    st.header("Update The People Table")
    current, new = st.columns(2)

    with current:
        currentref_name = st.text_input("Enter Current Reference Name")
        currentd_id = st.text_input("Enter Current Director's ID")
        currentyears = st.text_input("Enter Current years of work")
        currentlast_name = st.text_input("Enter Current Last Name")
        currentfirst_name = st.text_input("Enter Current First Name")
        currentyob = st.text_input("Enter Current year of Birth")
        currentyodeath = st.text_input("Enter Current Year of Death")


    with new:
        newref_name = st.text_input("Enter new Reference Name")
        newd_id = st.text_input("Enter new Director's ID")
        newyears = st.text_input("Enter new years of work")
        newlast_name = st.text_input("Enter new Last Name")
        newfirst_name = st.text_input("Enter new First Name")
        newyob = st.text_input("Enter new year of Birth")
        newyodeath = st.text_input("Enter new Year of Death")

    updateQuery = "UPDATE people set"
    if newref_name or newyears or newlast_name or newfirst_name or newd_id or newyob  or newyodeath:
        if newd_id:
            updateQuery = updateQuery + " d_id = '"+newd_id+"'"
        if newref_name:
            updateQuery = updateQuery + " ref_name = '" + newref_name + "'"
        if newyears:
            updateQuery = updateQuery + " years = '" + newyears +"'"
        if newlast_name:
            updateQuery = updateQuery + " last_name = '" + newlast_name + "'"
        if newfirst_name:
            updateQuery = updateQuery + " first_name = '" + newfirst_name + "'"
        if newyodeath:
            updateQuery = updateQuery + " yodeath = '" + newyodeath + "'"
        if newyob:
            updateQuery = updateQuery + " yob = '" + newyob + "'"
        if (currentref_name or currentd_id or currentyears or currentlast_name or currentfirst_name or currentyob  or currentyodeath):
            updateQuery = updateQuery + " WHERE"
            if currentfirst_name:
                updateQuery = updateQuery + " first_name = '"+currentfirst_name+"'"
            if currentyodeath:
                updateQuery = updateQuery + " yodeath = '"+ currentyodeath + "'"
            if currentref_name:
                updateQuery = updateQuery + " ref_name = '" + currentref_name + "'"
            if currentd_id:
                updateQuery = updateQuery + " d_id = '" + currentd_id +"'"
            if currentyears:
                updateQuery = updateQuery + " years = '" + currentyears + "'"
            if currentlast_name:
                updateQuery = updateQuery + " last_name = '" + currentlast_name + "'"
            if currentyob:
                updateQuery = updateQuery + " yob = '" + currentyob + "'"

    st.write(updateQuery)
    updateButton = st.button("Update People")

    if updateButton:
        if (currentref_name or currentd_id or currentyears or currentlast_name or currentfirst_name or currentyob   or currentyodeath) and (newref_name or newyears or newlast_name or newfirst_name or newd_id or newyob  or newyodeath):
            cur.execute(updateQuery)
            conn.commit()
            st.success("Update success")
        else:
            st.error("Please check before proceeding")

with tabDelete:
    st.header("Delete from People table")
    deleteref_name = st.text_input("Enter Reference Name of the person to delete")
    deleted_id = st.text_input("Enter Director's ID of the person to delete")
    deleteyears = st.text_input("Enter years of work of the person to delete")
    deletelast_name = st.text_input("Enter Last Name of the person to delete")
    deletefirst_name = st.text_input("Enter First Name of the person to delete")
    deleteyob = st.text_input("Enter Year of Birth of the person to delete")
    deleteyodeath = st.text_input("Enter Year of Death of the person to delete")

    deleteQuery = "DELETE from people where"
    if deleteref_name or deleted_id or deleteyears or deletelast_name or deletefirst_name or deleteyob  or deleteyodeath:
        if deletefirst_name:
            deleteQuery = deleteQuery + " first_name = '"+deletefirst_name+"'"
        if deleteref_name:
            deleteQuery = deleteQuery + " ref_name = '" + deleteref_name + "'"
        if deleted_id:
            deleteQuery = deleteQuery + " d_id = '" + deleted_id +"'"
        if deleteyears:
            deleteQuery = deleteQuery + " years = '" + deleteyears + "'"
        if deletelast_name:
            deleteQuery = deleteQuery + " last_name = '" + deletelast_name + "'"
        if deleteyodeath:
            deleteQuery = deleteQuery + " yodeath = '" + deleteyodeath + "'"
        if deleteyob:
            deleteQuery = deleteQuery + " yob = '" + deleteyob + "'"

    st.write(deleteQuery)
    deleteButton = st.button("Delete People")

    if deleteButton:
        if (deleteref_name or deleted_id or deleteyears or deletelast_name or deletefirst_name or deleteyob  or deleteyodeath):
            cur.execute(deleteQuery)
            conn.commit()
            st.success("Delete success")
        else:
            st.error("Please check before proceeding")

Connection.deleteConnection(conn,cur)