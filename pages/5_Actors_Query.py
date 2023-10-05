import streamlit as st
from Connection import *
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

conn, cur = Connection.createConnection()

st.title("Query Actors Table")

tabQuery, tabAdd, tabUpdate, tabDelete = st.tabs(["Query", "Add", "Update","Delete"])

with tabQuery:
    stagename = pd.read_sql("SELECT distinct stagename from actors",con=conn)
    yearsinwork = pd.read_sql("SELECT distinct yearsinwork from actors",con=conn)
    lastname = pd.read_sql("SELECT distinct lastname from actors",con=conn)
    firstname = pd.read_sql("SELECT distinct firstname from actors",con=conn)
    gender = pd.read_sql("SELECT distinct gender from actors",con=conn)
    yob = pd.read_sql("SELECT distinct yob from actors",con=conn)
    yod = pd.read_sql("SELECT distinct yod from actors",con=conn)
    roles = pd.read_sql("SELECT distinct roles from actors",con=conn)
    country = pd.read_sql("SELECT distinct country from actors",con=conn)

    st.header("Query the Actors table")
    st.markdown("<br>",unsafe_allow_html=True)

    stagename = st.multiselect("Select Stage Name", stagename,[])
    stagename_yearsinwork = st.selectbox(" ",["AND","OR"])
    yearsinwork = st.multiselect("Select yearsinWork for the industry",yearsinwork,[])
    yearsinwork_lastname = st.selectbox("  ",["AND","OR"])
    lastname = st.multiselect("Select lastname ",lastname,[])
    lastname_firstname = st.selectbox("       ",["AND","OR"])
    firstname = st.multiselect("Select firstname",firstname,[])
    firstname_gender = st.selectbox("   ",["AND","OR"])
    gender = st.multiselect("Select Gender",gender,[])
    gender_yob = st.selectbox("    ",["AND","OR"])
    yob = st.multiselect("Select Date of birth",yob,[])
    yob_yod = st.selectbox("                    ",["AND","OR"])
    yod = st.multiselect("Select Date of death",yod,[])
    yod_country = st.selectbox("             ",["AND","OR"])
    country = st.multiselect("Select country the actor is from",country,[])

    query = "SELECT * from actors"
    if stagename or gender or lastname or yob or firstname or yearsinwork or yod or country:
        query = query+" Where "

    if len(stagename)> 0:
        query = query +" (" 
        for i in stagename:
            
            if i is None:
                query = query+ " stagename is NULL or "
            else:
                query = query + "stagename = '"+i+"' or "
        query = query[:-3]+") "
        
    if len(yearsinwork)>0:
        if stagename:
            query = query + stagename_yearsinwork
        query = query+" ("
        for i in yearsinwork:
            if i is None:
                query = query+ " yearsinwork is NULL or "
            else:
                query = query + "yearsinwork = '"+i+"' or "
        query = query[:-3] +") "
        
    if len(lastname)>0:
        if stagename or lastname:
            query = query + yearsinwork_lastname
        query = query +" ("
        for i in lastname:
            if i is None:
                query = query+ " lastname is NULL or "
            else:
                query = query + " lastname = '"+i+"' or "
        query=query[:-3]+") "

    if len(firstname)>0:
        if stagename or lastname or yearsinwork:
            query = query + lastname_firstname
        query = query +" ("
        for i in firstname:
            if i is None:
                query = query+ " firstname is NULL or "
            else:
                query = query + " firstname = '"+i+"' or "
        query=query[:-3]+") "
    
    if len(gender)>0:
        if stagename or firstname or lastname or yearsinwork:
            query = query + firstname_gender
        query = query +" ("
        for i in firstname_gender:
            if i is None:
                query = query+ " gender is NULL or "
            else:
                query = query + " gender = '"+i+"' or "
        query=query[:-3]+") "

    if len(yob)>0:
        if stagename or firstname or lastname or gender or yearsinwork:
            query = query + gender_yob
        query = query +" ("
        for i in yob:
            if i is None:
                query = query+ " yob is NULL or "
            else:
                query = query + " yob = '"+i+"' or "
        query=query[:-3]+") "
    
    if len(yod)>0:
        if stagename or firstname or lastname or gender or yearsinwork or yob:
            query = query + gender_yob
        query = query +" ("
        for i in yod:
            if i is None:
                query = query+ " yod is NULL or "
            else:
                query = query + " yod = '"+i+"' or "
        query=query[:-3]+") "

    if len(country)>0:
        if stagename or firstname or lastname or gender or yearsinwork or yob or yod:
            query = query + gender_yob
        query = query +" ("
        for i in country:
            if i is None:
                query = query+ " country is NULL or "
            else:
                query = query + " country = '"+i+"' or "
        query=query[:-3]+") "

    st.write(query)
    result = pd.read_sql(query,con=conn)
    st.write(result)


with tabAdd:
    st.header("Add Actors")
    addstagename,addyearsinwork,addlastname,addfirstname,addgender,addyob, addyod, addcountry = 'Null','Null','Null', 'NULL', 'NULL','NULL','NULL','NULL'
    
    addstagename = st.text_input("Enter Stage Name")
    addyearsinwork = st.text_input("Enter yearsinwork for the industry")
    addlastname = st.text_input("Enter lastname")
    addfirstname = st.text_input("Enter firstname")
    addgender = st.text_input("Enter Gender")
    addyob = st.text_input("Enter Date of bith")
    addyod = st.text_input("Enter Date of Death")
    addcountry = st.text_input("Enter Country the actor is from")

    query = f"INSERT INTO actors (stagename, yearsinwork, lastname, gender, yob,firstname,yod,country) values ('{addstagename}','{addyearsinwork}','{addlastname}','{addgender}','{addyob}','{addfirstname}','{addyod}','{addcountry}')"
    st.write(query)
    addstudios = st.button("Add Actor")
    if addstudios:
        if addyearsinwork or addgender or addfirstname or addstagename or addlastname or addyob or addyod or addcountry:
            cur.execute(query)
            conn.commit()
            st.success("Actor added")
        else:
            st.error("Please check and try again")

with tabUpdate:
    st.header("Update The Actor Table")
    current, new = st.columns(2)

    with current:
        currentstagename = st.text_input("Enter Current Stage Name")
        currentyearsinwork = st.text_input("Enter Current yearsinwork ")
        currentlastname = st.text_input("Enter Current lastname")
        currentfirstname = st.text_input("Enter Current firstname")
        currentgender = st.text_input("Enter Current Gender")
        currentyob = st.text_input("Enter Current year of birth")
        currentyod = st.text_input("Enter Current year of death")
        currentcountry = st.text_input("Enter Current country")


    with new:
        newstagename = st.text_input("Enter new Stage Name")
        newyearsinwork = st.text_input("Enter new yearsinwork")
        newlastname = st.text_input("Enter new lastname ")
        newfirstname = st.text_input("Enter new firstname")
        newgender = st.text_input("Enter new Gender")
        newyob = st.text_input("Enter new year of birth")
        newyod = st.text_input("Enter new year of dath")
        newcountry = st.text_input("Enter new country")

    updateQuery = "UPDATE actors set"
    if newstagename or newlastname or newfirstname or newgender or newyearsinwork or newyob or newyod or newcountry:
        if newyearsinwork:
            updateQuery = updateQuery + " yearsinwork = '"+newyearsinwork+"'"
        if newstagename:
            updateQuery = updateQuery + " stagename = '" + newstagename + "'"
        if newlastname:
            updateQuery = updateQuery + " lastname = '" + newlastname +"'"
        if newfirstname:
            updateQuery = updateQuery + " firstname = '" + newfirstname + "'"
        if newgender:
            updateQuery = updateQuery + " gender = '" + newgender + "'"
        if newyob:
            updateQuery = updateQuery + " yob = '" + newyob + "'"
        if newyod:
            updateQuery = updateQuery + " yod = '" + newyod + "'"
        if newcountry:
            updateQuery = updateQuery + " country = '" + newcountry + "'"
        if (currentstagename or currentyearsinwork or currentlastname or currentfirstname or currentgender or currentyob or currentyod or currentcountry):
            updateQuery = updateQuery + " WHERE"
            if currentgender:
                updateQuery = updateQuery + " gender = '"+currentgender+"'"
            if currentstagename:
                updateQuery = updateQuery + " stagename = '" + currentstagename + "'"
            if currentyearsinwork:
                updateQuery = updateQuery + " yearsinwork = '" + currentyearsinwork +"'"
            if currentlastname:
                updateQuery = updateQuery + " lastname = '" + currentlastname + "'"
            if currentfirstname:
                updateQuery = updateQuery + " firstname = '" + currentfirstname + "'"
            if currentyob:
                updateQuery = updateQuery + " yob = '" + currentyob + "'"
            if currentyod:
                updateQuery = updateQuery + " yod = '" + currentyod + "'"
            if currentcountry:
                updateQuery = updateQuery + " country = '" + currentcountry + "'"

    st.write(updateQuery)
    updateButton = st.button("Update Actors")

    if updateButton:
        if (currentstagename or currentyearsinwork or currentlastname or currentfirstname or currentgender or currentyob or currentyod or currentcountry) and (newstagename or newlastname or newfirstname or newgender or newyearsinwork or newyob or newyod or newcountry):
            cur.execute(updateQuery)
            conn.commit()
            st.success("Update success")
        else:
            st.error("Please check before proceeding")

with tabDelete:
    st.header("Delete from actors table")
    deletestagename = st.text_input("Enter Stage Name of the actor to delete")
    deleteyearsinwork = st.text_input("Enter yearsinwork of the actor to delete")
    deletelastname = st.text_input("Enter lastname of the actor to delete")
    deletefirstname = st.text_input("Enter firstname of the actor to delete")
    deletegender = st.text_input("Enter Gender of the actor to delete")
    deleteyob = st.text_input("Enter Year of birth of the actor to delete")
    deleteyod = st.text_input("Enter Year of death of the actor to delete")
    deletecountry = st.text_input("Enter country of the actor to delete")

    deleteQuery = "DELETE from actors where"
    if deletestagename or deleteyearsinwork or deletelastname or deletefirstname or deletegender or deleteyob or deleteyod or deletecountry:
        if deletegender:
            deleteQuery = deleteQuery + " gender = '"+deletegender+"'"
        if deletestagename:
            deleteQuery = deleteQuery + " stagename = '" + deletestagename + "'"
        if deleteyearsinwork:
            deleteQuery = deleteQuery + " yearsinwork = '" + deleteyearsinwork +"'"
        if deletelastname:
            deleteQuery = deleteQuery + " lastname = '" + deletelastname + "'"
        if deletefirstname:
            deleteQuery = deleteQuery + " firstname = '" + deletefirstname + "'"
        if deleteyob:
            deleteQuery = deleteQuery + " yob = '" + deleteyob + "'"
        if deleteyod:
            deleteQuery = deleteQuery + " yod = '" + deleteyod + "'"
        if deletecountry:
            deleteQuery = deleteQuery + " country = '" + deletecountry + "'"

    st.write(deleteQuery)
    deleteButton = st.button("Delete Actor")

    if deleteButton:
        if (deletestagename or deleteyearsinwork or deletelastname or deletefirstname or deletegender or deleteyob):
            cur.execute(deleteQuery)
            conn.commit()
            st.success("Delete success")
        else:
            st.error("Please check before proceeding")

Connection.deleteConnection(conn,cur)