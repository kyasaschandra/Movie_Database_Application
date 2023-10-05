import streamlit as st
from Connection import *
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

conn,cur= Connection.createConnection()

st.title("Query Movies Table")

tabQuery, tabAdd, tabUpdate, tabDelete = st.tabs(["Query", "Add", "Update","Delete"])

with tabQuery:
    directors = pd.read_sql("SELECT distinct director from movies",con=conn)
    producers = pd.read_sql("SELECT distinct producers from movies",con=conn)
    studios = pd.read_sql("SELECT distinct studios from movies",con=conn)
    years = pd.read_sql("SELECT distinct release_year from movies order by release_year",con=conn)
    cats = pd.read_sql("SELECT category from categories",con=conn)
    proc = pd.read_sql("SELECT fullname from colorcodes",con=conn)
    awards = pd.read_sql("SELECT award from awardstype",con=conn)
    st.header("Query the Movies table")
    st.markdown("<br>",unsafe_allow_html=True)

    directors = st.multiselect("Select Directors", directors,[])
    director_producers = st.selectbox(" ",["AND","OR"])
    producers = st.multiselect("Select Producers",producers,[])
    producers_studio = st.selectbox("  ",["AND","OR"])
    studios = st.multiselect("Select Studio",studios,[])
    studio_years = st.selectbox("       ",["AND","OR"])
    years = st.multiselect("Select release years",years,[])
    years_category = st.selectbox("   ",["AND","OR"])
    cats = st.multiselect("Select Category",cats,[])
    category_proc = st.selectbox("    ",["AND","OR"])
    proc = st.multiselect("Select Process",proc,[])
    proc_awards = st.selectbox("                  ",["AND","OR"])
    awards = st.multiselect("Select award",awards,[])

    query = "SELECT * from movies"
    if directors or producers or years or cats or proc or studios or awards:
        query = query+" Where "

    if len(directors)> 0:
        query = query +" (" 
        for i in directors:
            
            if i is None:
                query = query+ " director is NULL or "
            else:
                query = query + "director = '"+i+"' or "
        query = query[:-3]+") "
        
    if len(producers)>0:
        if directors:
            query = query + director_producers
        query = query+" ("
        for i in producers:
            if i is None:
                query = query+ " producers is NULL or "
            else:
                query = query + "producers = '"+i+"' or "
        query = query[:-3] +") "
        
    if len(studios)>0:
        if directors or producers:
            query = query + producers_studio
        query = query +" ("
        for i in studios:
            if i is None:
                query = query+ " studios is NULL or "
            else:
                query = query + " studios = '"+i+"' or "
        query=query[:-3]+") "

    if len(years)>0:
        if directors or producers or studios:
            query = query + producers_studio
        query = query +" ("
        for i in years:
            if i is None:
                query = query+ " release_year is NULL or "
            else:
                query = query + " release_year = '"+i+"' or "
        query=query[:-3]+") "
    
    if len(cats)>0:
        if directors or producers or years or studios:
            query = query + years_category
        query = query +" ("
        for i in cats:
            jquery = "Select code from categories where category = '" + i+"'"
            cur.execute(jquery)
            j = cur.fetchall()
            j = list(j)
            if i is None:
                query = query+ " category is NULL or "
            else:
                query = query + " category = '"+j[0][0]+"' or "
        query=query[:-3]+") "

    if len(proc)>0:
        if directors or producers or years or cats or studios:
            query = query + category_proc
        query = query +" ("
        for i in proc:
            jquery = "Select code from colorcodes where fullname = '" + i+"'"
            cur.execute(jquery)
            j = cur.fetchall()
            j = list(j)
            if i is None:
                query = query+ " process is NULL or "
            else:
                query = query + " process = '"+j[0][0]+"' or "
        query=query[:-3]+") "
    
    if len(awards)>0:
        if directors or producers or years or cats or studios or proc:
            query = query + proc_awards
        query = query +" ("
        for i in awards:
            if i is None:
                query = query+ " awards is NULL or "
            else:
                query = query + " awards = '"+i+"' or "
        query=query[:-3]+") "

    st.write(query)
    result = pd.read_sql(query,con=conn)
    st.write(result)



with tabAdd:
    addpeople = pd.read_sql("Select distinct ref_name from people",con=conn)
    addstudios = pd.read_sql("SELECT distinct studios from movies",con=conn)
    addcats = pd.read_sql("SELECT category from categories",con=conn)
    addproc = pd.read_sql("SELECT fullname from colorcodes",con=conn)
    addawards = pd.read_sql("SELECT award from awardstype",con=conn)

    st.header("Add Movies")
    addFilmId, addtitle, addDirector, addProducer,addstudio,addyear,addCats,addProc,addAwards = 'Null', 'NULL', 'NULL','NULL','NULL','NULL','NULL','NULL','NULL'
    
    st.warning("Make sure to add new Directors and Producers to People table and New Studios to studios table")
    addFilmId = st.text_input("Enter ID for the movie")
    addtitle = st.text_input("Enter movie name")
    addDirector = st.selectbox("Enter Director Name",addpeople)
    addProducer = st.selectbox("Enter Producer Name",addpeople)
    addstudio = st.selectbox("Enter Studio Name",addstudios)
    addyear = st.select_slider("Select year released",list(range(1800,2024)))
    addCats = st.selectbox("Select category",addcats)
    addProc = st.selectbox("Select Process",addproc)
    addAwards = st.selectbox("Select Award recived",addawards)

    catsquery = "Select code from categories where category = '" + addCats+"'"
    cur.execute(catsquery)
    j = cur.fetchall()
    addCats = list(j)[0][0]

    procquery = "Select code from colorcodes where fullname = '" + addProc+"'"
    cur.execute(procquery)
    j = cur.fetchall()
    addProc = list(j)[0][0]

    query = f"insert into movies (film_id, title, release_year, director, producers, studios, process, category, awards) values ('{addFilmId}','{addtitle}','{addyear}','{addDirector}','{addProducer}','{addstudio}','{addProc}','{addCats}','{addAwards}')"
    st.write(query)
    addMovie = st.button("Add Movie")
    if addMovie:
        if addFilmId or addtitle or addDirector or addProducer or addstudio or addyear or addCats or addProc or addAwards:    
            cur.execute(query)
            conn.commit()
            st.success("Movie added")
        else:
            st.error("Please check and Try again")


with tabUpdate:
    st.header("Update the Movie Table")
    current, new = st.columns(2)
    # updatepeople = pd.read_sql("Select distinct ref_name from people",con=conn)
    # updatestudios = pd.read_sql("SELECT distinct studios from movies",con=conn)
    # updatecats = pd.read_sql("SELECT category from categories",con=conn)
    # updateproc = pd.read_sql("SELECT fullname from colorcodes",con=conn)
    # updateawards = pd.read_sql("SELECT award from awardstype",con=conn)
    # updatetitle = pd.read_sql("Select title from movies", con=conn)
    # updateFilm_id = pd.read_sql("select film_id from movies", con=conn)
    st.warning("Make sure that all the current and new attributes are already in the respective tables")
    st.warning("Please enter the award, category and process in code that are present in tables")
    current, new = st.columns(2)

    with current:
        oldupdatefilm_id = st.text_input("Enter Current Film_Id")
        oldupdatetitle = st.text_input("Enter Current Title")
        oldupdateyear = st.text_input("Enter Current Release year")
        oldupdateDirector = st.text_input("Enter Current Director")
        oldupdateProducer = st.text_input("Enter Current Producer")
        oldupdateStudio = st.text_input("Enter Current Studio")
        oldupdateCats = st.text_input("Enter Current Category code")
        oldupdateProc = st.text_input("Enter Current Process code")
        oldupdateAwards = st.text_input("Enter Current Awards recieved")


    with new:
        newupdatefilm_id = st.text_input("Enter New Film_Id")
        newupdatetitle = st.text_input("Enter New Title")
        newupdateyear = st.text_input("Enter New Release year")
        newupdateDirector = st.text_input("Enter New Director")
        newupdateProducer = st.text_input("Enter New Producer")
        newupdateStudio = st.text_input("Enter New Studio")
        newupdateCats = st.text_input("Enter New Category code")
        newupdateProc = st.text_input("Enter New Process code")
        newupdateAwards = st.text_input("Enter New Awards recieved")

    updateQuery = "UPDATE movies set"
    if newupdateyear or newupdateAwards or newupdateCats or newupdateDirector or newupdatefilm_id or newupdateProc  or newupdateProducer or newupdateStudio or newupdatetitle:
        if newupdatefilm_id:
            updateQuery = updateQuery + " film_id = '"+newupdatefilm_id+"'"
        if newupdatetitle:
            updateQuery = updateQuery + " title = '"+ newupdatetitle + "'"
        if newupdateyear:
            updateQuery = updateQuery + " release_year = '" + newupdateyear + "'"
        if newupdateAwards:
            updateQuery = updateQuery + " awards = '" + newupdateAwards +"'"
        if newupdateCats:
            updateQuery = updateQuery + " Category = '" + newupdateCats + "'"
        if newupdateDirector:
            updateQuery = updateQuery + " director = '" + newupdateDirector + "'"
        if newupdateProducer:
            updateQuery = updateQuery + " producers = '" + newupdateProducer + "'"
        if newupdateProc:
            updateQuery = updateQuery + " process = '" + newupdateProc + "'"
        if newupdateStudio:
            updateQuery = updateQuery + " studios = '" + newupdateStudio + ""
        if (oldupdateyear or oldupdateAwards or oldupdateCats or oldupdateDirector or oldupdatefilm_id or oldupdateProc  or oldupdateProducer or oldupdateStudio or oldupdatetitle):
            updateQuery = updateQuery + " WHERE"
            if oldupdatefilm_id:
                updateQuery = updateQuery + " film_id = '"+oldupdatefilm_id+"'"
            if oldupdatetitle:
                updateQuery = updateQuery + " title = '"+ oldupdatetitle + "'"
            if oldupdateyear:
                updateQuery = updateQuery + " release_year = '" + oldupdateyear + "'"
            if oldupdateAwards:
                updateQuery = updateQuery + " awards = '" + oldupdateAwards +"'"
            if oldupdateCats:
                updateQuery = updateQuery + " Category = '" + oldupdateCats + "'"
            if oldupdateDirector:
                updateQuery = updateQuery + " director = '" + oldupdateDirector + "'"
            if oldupdateProducer:
                updateQuery = updateQuery + " producers = '" + oldupdateProducer + "'"
            if oldupdateProc:
                updateQuery = updateQuery + " process = '" + oldupdateProc + "'"
            if oldupdateStudio:
                updateQuery = updateQuery + " studios = '" + oldupdateStudio + ""

    st.write(updateQuery)
    updateButton = st.button("Update Movie")

    if updateButton:
        if (oldupdateyear or oldupdateAwards or oldupdateCats or oldupdateDirector or oldupdatefilm_id or oldupdateProc  or oldupdateProducer or oldupdateStudio or oldupdatetitle) and (newupdateyear or newupdateAwards or newupdateCats or newupdateDirector or newupdatefilm_id or newupdateProc  or newupdateProducer or newupdateStudio or newupdatetitle):
            cur.execute(updateQuery)
            conn.commit()
            st.success("Update success")
        else:
            st.error("Please check before proceeding")


with tabDelete:
    st.header("Delete from Movies table")
    deletefilm_id = st.text_input("Enter ID for the movie to delete")
    deletetitle = st.text_input("Enter movie name to delete")
    deleteDirector = st.text_input("Enter Director Name to delete")
    deleteProducer = st.text_input("Enter Producer Name to delete")
    deleteStudio = st.text_input("Enter Studio Name to delete")
    deleteyear = st.text_input("Enter year released to delete")
    deleteCats = st.text_input("Enter category to delete")
    deleteProc = st.text_input("Enter Process to delete")
    deleteAwards = st.text_input("Enter Award recived to delete")

    deleteQuery = "DELETE from movies where"
    if deleteyear or deleteAwards or deleteCats or deleteDirector or deletefilm_id or deleteProc  or deleteProducer or deleteStudio or deletetitle:
        if deletefilm_id:
            deleteQuery = deleteQuery + " film_id = '"+deletefilm_id+"'"
        if deletetitle:
            deleteQuery = deleteQuery + " title = '"+ deletetitle + "'"
        if deleteyear:
            deleteQuery = deleteQuery + " release_year = '" + deleteyear + "'"
        if deleteAwards:
            deleteQuery = deleteQuery + " awards = '" + deleteAwards +"'"
        if deleteCats:
            deleteQuery = deleteQuery + " Category = '" + deleteCats + "'"
        if deleteDirector:
            deleteQuery = deleteQuery + " director = '" + deleteDirector + "'"
        if deleteProducer:
            deleteQuery = deleteQuery + " producers = '" + deleteProducer + "'"
        if deleteProc:
            deleteQuery = deleteQuery + " process = '" + deleteProc + "'"
        if deleteStudio:
            deleteQuery = deleteQuery + " studios = '" + deleteStudio + ""

    st.write(deleteQuery)
    deleteButton = st.button("Delete Movie")

    if deleteButton:
        if (deleteyear or deleteAwards or deleteCats or deleteDirector or deletefilm_id or deleteProc  or deleteProducer or deleteStudio or deletetitle):
            cur.execute(deleteQuery)
            conn.commit()
            st.success("Delete success")
        else:
            st.error("Please check before proceeding")

Connection.deleteConnection(conn,cur)