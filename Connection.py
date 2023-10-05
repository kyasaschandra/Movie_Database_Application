import psycopg2
from insertClass import *
class Connection:
    hostname = 'localhost'
    database = 'DMQL TEST 3'
    username = 'postgres'
    pwd = 'yasas'
    port_id = 5432
    cur = None
    conn= None

    def createConnection():
        conn = psycopg2.connect(host=Connection.hostname,dbname=Connection.database,
                                        user = Connection.username, password=Connection.pwd,
                                        port = Connection.port_id)
        cur= conn.cursor()
        return conn, cur
    
    def deleteConnection(conn, cur):
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

    def insert():
        try:
            conn, cur = Connection.createConnection()
            insertvalues = insertValues
            insertvalues.insertGeography(cur,conn)
            insertvalues.insertCategories(cur,conn)
            insertvalues.insertColorcodes(cur,conn)
            insertvalues.insertAwards(cur,conn)
            insertvalues.insertStudios(cur,conn)
            insertvalues.insertPeople(cur,conn)
            insertvalues.insertActors(cur,conn)
            insertvalues.insertMovies(cur,conn)
            insertvalues.insertRoletypes(cur,conn)
            insertvalues.insertCasts(cur,conn)

        except Exception as e:
            print(e)
        finally:
            Connection.deleteConnection(conn,cur)




