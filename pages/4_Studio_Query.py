import streamlit as st
from Connection import *
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

conn, cur = Connection.createConnection()

st.title("Query Studio Table")

tabQuery, tabAdd, tabUpdate, tabDelete = st.tabs(["Query", "Add", "Update","Delete"])

with tabQuery:
    studioname = pd.read_sql("SELECT distinct studioname from studios",con=conn)
    company = pd.read_sql("SELECT distinct company from studios",con=conn)
    city = pd.read_sql("SELECT distinct city from studios",con=conn)
    country = pd.read_sql("SELECT distinct country from studios",con=conn)
    foundeddate = pd.read_sql("SELECT distinct foundeddate from studios",con=conn)
    enddate = pd.read_sql("SELECT distinct enddate from studios",con=conn)
    st.header("Query the studios table")
    st.markdown("<br>",unsafe_allow_html=True)

    studioname = st.multiselect("Select Studio Name", studioname,[])
    studioname_company = st.selectbox(" ",["AND","OR"])
    company = st.multiselect("Select Comapnay Name",company,[])
    company_city = st.selectbox("  ",["AND","OR"])
    city = st.multiselect("Select City Studio is Locateed",city,[])
    city_country = st.selectbox("       ",["AND","OR"])
    country = st.multiselect("Select Country",country,[])
    country_foundeddate = st.selectbox("   ",["AND","OR"])
    foundeddate = st.multiselect("Select Date Founded",foundeddate,[])
    foundeddate_enddate = st.selectbox("    ",["AND","OR"])
    enddate = st.multiselect("Select Date when the Studio closed",enddate,[])

    query = "SELECT * from studios"
    if studioname or foundeddate or city or enddate or country or company:
        query = query+" Where "

    if len(studioname)> 0:
        query = query +" (" 
        for i in studioname:
            
            if i is None:
                query = query+ " studioname is NULL or "
            else:
                query = query + "studioname = '"+i+"' or "
        query = query[:-3]+") "
        
    if len(company)>0:
        if studioname:
            query = query + studioname_company
        query = query+" ("
        for i in company:
            if i is None:
                query = query+ " company is NULL or "
            else:
                query = query + "company = '"+i+"' or "
        query = query[:-3] +") "
        
    if len(city)>0:
        if studioname or city:
            query = query + company_city
        query = query +" ("
        for i in city:
            if i is None:
                query = query+ " city is NULL or "
            else:
                query = query + " city = '"+i+"' or "
        query=query[:-3]+") "

    if len(country)>0:
        if studioname or city or company:
            query = query + city_country
        query = query +" ("
        for i in country:
            if i is None:
                query = query+ " country is NULL or "
            else:
                query = query + " country = '"+i+"' or "
        query=query[:-3]+") "
    
    if len(foundeddate)>0:
        if studioname or country or city or company:
            query = query + country_foundeddate
        query = query +" ("
        for i in country_foundeddate:
            if i is None:
                query = query+ " foundeddate is NULL or "
            else:
                query = query + " foundeddate = '"+i+"' or "
        query=query[:-3]+") "

    if len(enddate)>0:
        if studioname or country or city or foundeddate or company:
            query = query + foundeddate_enddate
        query = query +" ("
        for i in enddate:
            if i is None:
                query = query+ " enddate is NULL or "
            else:
                query = query + " enddate = '"+i+"' or "
        query=query[:-3]+") "

    st.write(query)
    result = pd.read_sql(query,con=conn)
    st.write(result)


with tabAdd:
    st.header("Add studios")
    addstudioname,addcompany,addcity,addcountry,addfoundeddate,addenddate = 'Null', 'NULL', 'NULL','NULL','NULL','NULL'
    
    addstudioname = st.text_input("Enter Studio Name")
    addcompany = st.text_input("Enter Company Name")
    addcity = st.text_input("Enter city")
    addcountry = st.text_input("Enter Country")
    addfoundeddate = st.text_input("Enter Date Founded")
    addenddate = st.text_input("Enter Date studio closed")

    query = f"INSERT INTO studios (studioname, company, city, foundeddate, enddate,country) values ('{addstudioname}','{addcompany}','{addcity}','{addfoundeddate}','{addenddate}','{addcountry}')"
    st.write(query)
    addstudios = st.button("Add studio")
    if addstudios:
        if addcompany or addfoundeddate or addcountry or addstudioname or addcity or addenddate:
            cur.execute(query)
            conn.commit()
            st.success("studio added")
        else:
            st.error("Please check and try again")

with tabUpdate:
    st.header("Update The studios Table")
    current, new = st.columns(2)

    with current:
        currentstudioname = st.text_input("Enter Current Studio Name")
        currentcompany = st.text_input("Enter Current Company Name")
        currentcity = st.text_input("Enter Current city")
        currentcountry = st.text_input("Enter Current Country")
        currentfoundeddate = st.text_input("Enter Current Founded date")
        currentenddate = st.text_input("Enter Current date studio Closed")


    with new:
        newstudioname = st.text_input("Enter new Studio Name")
        newcompany = st.text_input("Enter new company's Name")
        newcity = st.text_input("Enter new city ")
        newcountry = st.text_input("Enter new Country")
        newfoundeddate = st.text_input("Enter new Founded date")
        newenddate = st.text_input("Enter new date studio closed")

    updateQuery = "UPDATE studios set"
    if newstudioname or newcity or newcountry or newfoundeddate or newcompany or newenddate:
        if newcompany:
            updateQuery = updateQuery + " company = '"+newcompany+"'"
        if newstudioname:
            updateQuery = updateQuery + " studioname = '" + newstudioname + "'"
        if newcity:
            updateQuery = updateQuery + " city = '" + newcity +"'"
        if newcountry:
            updateQuery = updateQuery + " country = '" + newcountry + "'"
        if newfoundeddate:
            updateQuery = updateQuery + " foundeddate = '" + newfoundeddate + "'"
        if newenddate:
            updateQuery = updateQuery + " enddate = '" + newenddate + "'"
        if (currentstudioname or currentcompany or currentcity or currentcountry or currentfoundeddate or currentenddate):
            updateQuery = updateQuery + " WHERE"
            if currentfoundeddate:
                updateQuery = updateQuery + " foundeddate = '"+currentfoundeddate+"'"
            if currentstudioname:
                updateQuery = updateQuery + " studioname = '" + currentstudioname + "'"
            if currentcompany:
                updateQuery = updateQuery + " company = '" + currentcompany +"'"
            if currentcity:
                updateQuery = updateQuery + " city = '" + currentcity + "'"
            if currentcountry:
                updateQuery = updateQuery + " country = '" + currentcountry + "'"
            if currentenddate:
                updateQuery = updateQuery + " enddate = '" + currentenddate + "'"

    st.write(updateQuery)
    updateButton = st.button("Update studios")

    if updateButton:
        if (currentstudioname or currentcompany or currentcity or currentcountry or currentfoundeddate or currentenddate) and (newstudioname or newcity or newcountry or newfoundeddate or newcompany or newenddate):
            cur.execute(updateQuery)
            conn.commit()
            st.success("Update success")
        else:
            st.error("Please check before proceeding")

with tabDelete:
    st.header("Delete from studios table")
    deletestudioname = st.text_input("Enter Studio Name of the studio to delete")
    deletecompany = st.text_input("Enter Company's Name of the studio to delete")
    deletecity = st.text_input("Enter city of the studio to delete")
    deletecountry = st.text_input("Enter Country of the studio to delete")
    deletefoundeddate = st.text_input("Enter Founded Date of the studio to delete")
    deleteenddate = st.text_input("Enter Date closed of the studio to delete")

    deleteQuery = "DELETE from studios where"
    if deletestudioname or deletecompany or deletecity or deletecountry or deletefoundeddate or deleteenddate:
        if deletefoundeddate:
            deleteQuery = deleteQuery + " foundeddate = '"+deletefoundeddate+"'"
        if deletestudioname:
            deleteQuery = deleteQuery + " studioname = '" + deletestudioname + "'"
        if deletecompany:
            deleteQuery = deleteQuery + " company = '" + deletecompany +"'"
        if deletecity:
            deleteQuery = deleteQuery + " city = '" + deletecity + "'"
        if deletecountry:
            deleteQuery = deleteQuery + " country = '" + deletecountry + "'"
        if deleteenddate:
            deleteQuery = deleteQuery + " enddate = '" + deleteenddate + "'"

    st.write(deleteQuery)
    deleteButton = st.button("Delete studios")

    if deleteButton:
        if (deletestudioname or deletecompany or deletecity or deletecountry or deletefoundeddate or deleteenddate):
            cur.execute(deleteQuery)
            conn.commit()
            st.success("Delete success")
        else:
            st.error("Please check before proceeding")

Connection.deleteConnection(conn,cur)