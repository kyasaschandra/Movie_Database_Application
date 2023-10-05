from time import sleep
import pandas as pd
import numpy as np
class insertValues:

    def insertMovies(cur,conn):
        query="""CREATE TABLE movies
                (
                    film_id varchar(20) NOT NULL,
                    title varchar(200) NOT NULL,
                    release_year varchar(5),
                    director varchar(100),
                    producers varchar(100),
                    studios varchar(100),
                    process varchar(10),
                    category varchar(10),
                    awards varchar(50),
                    CONSTRAINT movies_pkey PRIMARY KEY (film_id),
                    CONSTRAINT movies_awards_fkey FOREIGN KEY (awards)
                        REFERENCES public.awardstype (award) MATCH SIMPLE
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT movies_category_fkey FOREIGN KEY (category)
                        REFERENCES public.categories (code) MATCH SIMPLE
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT movies_director_fkey FOREIGN KEY (director)
                        REFERENCES public.people (ref_name) MATCH SIMPLE
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT movies_process_fkey FOREIGN KEY (process)
                        REFERENCES public.colorcodes (code) MATCH SIMPLE
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT movies_producers_fkey FOREIGN KEY (producers)
                        REFERENCES public.people (ref_name) MATCH SIMPLE
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CONSTRAINT movies_studios_fkey FOREIGN KEY (studios)
                        REFERENCES public.studios (studioname) MATCH SIMPLE
                        ON UPDATE CASCADE ON DELETE CASCADE
                );"""
        cur.execute(query)
        # file = pd.read_csv('main.csv',delimiter=';',header=None)
        file = pd.read_excel('main.xlsx')
        
        def transformRows(row):
            try:
                col6 = row[5]
                col6 = col6.split(';')[0]
                col6 = col6.split(':')
                if len(col6)>1:
                    col6 = col6[1]
                else:
                    row[5] = np.nan
                    return row
                col6 = col6.split(',')[0]
                row[5] = col6
                return row
            except Exception as e:
                return row
            
        def transformCol4(row):
            col4 = row[3]
            try:
                row[3]=col4.split(':')[1]
                if ' ' in row[3]:
                    row[3] = row[3].split(' ')[0]
                if ',' in row[3]:
                    row[3] = row[3].split(',')[0]
                return row
            except:
                return row
            
        def transformCol5(row):
            col5 =row[4]
            try:
                col5=col5.split(':')
                if len(col5)>1:
                    col5 = col5[1]
                else:
                    row[5] = np.nan
                    return row
                col5 = col5.split(',')[0]
                row[4]=col5
                return row
            except:
                return row
        
        def transformCol7(row):
            col6 = row[6]
            try:
                if ' ' in col6:
                    col6=col6.split(' ')[0]
                if ',' in col6:
                    col6=col6.split(',')[0]
                row[6]=col6
                return row
            except:
                return row

        def transformColCat(row):
            col8 = row[7]
            try:
                if ' ' in col8:
                    col8=col8.split(' ')[0]
                if ',' in col8:
                    col8 = col8.split(',')[0]
                row[7] = col8
                if row[7] == "SciF":
                    row[7] = "S.F."
                return row
            except:
                if row[7] == "SciF":
                        row[7] = "S.F."
                return row
        
        def transformColAw(row):
            col8 = row[8]
            try:
                if ' ' in col8:
                    col8 = col8.split(' ')[0]
                if ',' in col8:
                    col8 = col8.split(',')[0]
                row[8]=col8
            except:
                pass
            finally:
                return row
            
        file = file.apply(lambda row: transformRows(row), axis=1)
        file = file.apply(lambda row: transformCol4(row), axis=1)
        file = file.apply(lambda row: transformCol5(row), axis=1)
        file = file.apply(lambda row: transformCol7(row), axis=1)
        file = file.apply(lambda row: transformColCat(row),axis=1)
        file = file.apply(lambda row: transformColAw(row),axis=1)

        def convertString(row):
            for i in range(9):
                row[i]="'"+str(row[i])+"'"
                if row[i]=="'nan'" or row[i]==np.nan or row[i]=="''" or 'none' in row[i]:
                    row[i]="NULL"
                
            return row
        
        file = file.apply(lambda row: convertString(row), axis=1)

        def insertRows(intext):
            try:
                insertquery = "INSERT INTO movies (film_id, title, release_year, director, producers, studios, process, category, awards) VALUES ("+intext[0]+","+intext[1]+","+intext[2]+","+intext[3]+","+intext[4]+","+intext[5]+","+intext[6]+","+intext[7]+","+intext[8]+")"
                #print(insertquery)
                cur.execute(insertquery)
                conn.commit()
            except Exception as e:
                #print(e)
                #print(insertquery)
                #print()
                conn.rollback()
                if 'not present' in str(e):
                    if '(studios)' in str(e):
                        #print(intext[5])
                        intext[5] = "NULL"
                        insertRows(intext)
                    elif '(producers)' in str(e):
                        intext[4] = "NULL"
                        insertRows(intext)
                    elif '(director)' in str(e):
                        intext[3] = "NULL"
                        insertRows(intext)
                    #else:
                        #print()
                        #print(e)
                        #print(insertquery)
                #sleep(2)
                
        file.apply(lambda row: insertRows(row), axis=1)
        
        

    def insertActors(cur,conn):
        query = """CREATE TABLE actors
                    (
                        stagename varchar(50) NOT NULL,
                        yearsinwork varchar(10),
                        lastname varchar(50),
                        firstname varchar(50),
                        gender character(1),
                        yob varchar(5),
                        yod varchar(5),
                        roles varchar(100),
                        country varchar(3),
                        CONSTRAINT actors_pkey PRIMARY KEY (stagename),
                        CONSTRAINT actors_country_fkey FOREIGN KEY (country)
                            REFERENCES public.geography (code) MATCH SIMPLE
                            ON UPDATE CASCADE
                            ON DELETE CASCADE
                    );"""
        cur.execute(query)
        with open('actors.csv','r') as f:
            for line in f:
                intext = line[:-1].split(';')
                for i in range(len(intext)):
                    if intext[i] == '""' or intext[i] == '"Un"' or '[' in intext[i]:
                        intext[i] = '"NULL"'
                    if '-Am' in intext[8]:
                        intext[8] = '"Am"'
                    intext[i]=intext[i][1:-1]
                if ':' in intext[7] :
                    intext[7] =intext[7].split(':')[1]
                insertquery = "INSERT INTO actors (stagename, yearsinwork, lastname, firstname, gender, yob, yod, roles, country) VALUES ('"+intext[0].replace("\"","\'")+"','"+intext[1].replace("\"","\'")+"','"+intext[2].replace("\"","\'")+"','"+intext[3].replace("\"","\'")+"','"+intext[4].replace("\"","\'")+"','"+intext[5].replace("\"","\'")+"','"+intext[6].replace("\"","\'")+"','"+intext[7].replace("\"","\'")+"','"+intext[8].replace("\"","\'")+"')"
                #print(insertquery)
                try:
                    cur.execute(insertquery)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(e)
        print("Actors done")

    # def insertPeople(cur,conn):
    #     query = """CREATE TABLE people
    #                 (
    #                     ref_name varchar(50) NOT NULL,
    #                     codes varchar(10) NOT NULL,
    #                     d_id varchar(10),
    #                     years varchar(50),
    #                     last_name varchar(50),
    #                     first_name varchar(50),
    #                     yob varchar(5),
    #                     yodeath varchar(5),
    #                     CONSTRAINT people_pkey PRIMARY KEY (ref_name,codes),
    #                     CONSTRAINT people_codes_fkey FOREIGN KEY (codes) 
    #                         REFERENCES peoplecode (code) MATCH SIMPLE
    #                         ON UPDATE CASCADE
    #                         ON DELETE CASCADE
    #                 );"""
    #     cur.execute(query)
    #     with open("people.csv",'r') as f:
    #         for line in f:
    #             intext = line[:-1].split(';')
    #             if len(intext[3])>2:
    #                intext[3]="\""+intext[3][1:].strip('@')
    #             for i in range(len(intext)):
    #                 if intext[i] == '""' or intext[i] == '"Un"' or '[' in intext[i]:
    #                     intext[i] = 'NULL'
    #             for i in intext[1][1:-1]:
    #                 insertquery = "INSERT INTO people (ref_name, codes, d_id, years, last_name, first_name, yob, yodeath) VALUES ("+intext[0].replace("\"","\'")+",'"+i+"',"+intext[2].replace("\"","\'")+","+intext[3].replace("\"","\'")+","+intext[4].replace("\"","\'")+","+intext[5].replace("\"","\'")+","+intext[6].replace("\"","\'")+","+intext[7].replace("\"","\'")+")"
    #                 print(insertquery)
    #                 cur.execute(insertquery)
    #                 conn.commit() 
    #         f.close()

    def insertPeople(cur,conn):
        query = """CREATE TABLE people
                    (
                        ref_name varchar(50) NOT NULL,
                        d_id varchar(10),
                        years varchar(50),
                        last_name varchar(50),
                        first_name varchar(50),
                        yob varchar(5),
                        yodeath varchar(5),
                        CONSTRAINT people_pkey PRIMARY KEY (ref_name)
                    );"""
        cur.execute(query)
        with open("people.csv",'r') as f:
            for line in f:
                intext = line[:-1].split(';')
                if len(intext[3])>2:
                   intext[3]="\""+intext[3][1:].strip('@')
                for i in range(len(intext)):
                    if intext[i] == '""' or intext[i] == '"Un"' or '[' in intext[i]:
                        intext[i] = 'NULL'
                
                insertquery = "INSERT INTO people (ref_name, d_id, years, last_name, first_name, yob, yodeath) VALUES ("+intext[0].replace("\"","\'")+","+intext[2].replace("\"","\'")+","+intext[3].replace("\"","\'")+","+intext[4].replace("\"","\'")+","+intext[5].replace("\"","\'")+","+intext[6].replace("\"","\'")+","+intext[7].replace("\"","\'")+")"
                #print(insertquery)
                cur.execute(insertquery)
                conn.commit() 
            f.close()
        print("People done")

    def insertStudios(cur,conn):
        createStu = """CREATE TABLE studios
(
    studioname varchar(50) NOT NULL,
    company varchar(100),
    city varchar(50),
    country varchar(50) references geography (code),
    foundeddate varchar(20),
    enddate varchar(20),
    CONSTRAINT studios_pkey PRIMARY KEY (studioname)
);"""
        cur.execute(createStu)
        with open("studios.csv","r") as f:
            for line in f:
                intext = line[:-1].split(';')
                for i in range(len(intext)):
                    if intext[i] == '""':
                        intext[i] = 'NULL'
                if intext[3] == '"USA"' or intext[3] == '"U.S.A."' or intext[3] == '"NY"':
                    intext[3] = '"Am"'
                if intext[3] == '"France"':
                    intext[3] = '"Fr"'
                if intext[3] == '"Germany"' or intext[3] == '"Holland"':
                    intext[3] = '"Ge"'
                if intext[3] == '"Italy"':
                    intext[3] = '"It"'
                if intext[3] == '"Cuba"':
                    intext[3] = '"Cu"'
                if intext[3] == '"Australia"':
                    intext[3] = '"Au"'
                if intext[3] == '"Denmark"':
                    intext[3] = '"Da"'
                if intext[3] == '"India"':
                    intext[3] = '"In"'
                if intext[3] == '"China"':
                    intext[3] = '"Ch"'
                if intext[3] == '"England"' or intext[3] == '"UK"':
                    intext[3] = '"GB"'

                if '?' in intext[4]:
                    intext[4]=intext[4][:-1].strip('?')+"'"
                if '+' in intext[4]:
                    intext[4]=intext[4][:-1].strip('+')+"'"
                if '-' in intext[4]:
                    intext[4]=intext[4][:-1].strip('-')+"'"

                if '?' in intext[5]:
                    intext[5]=intext[5][:-1].strip('?')+"'"
                if '+' in intext[5]:
                    intext[5]=intext[5][:-1].strip('+')+"'"
                if '-' in intext[5]:
                    intext[5]=intext[5][:-1].strip('-')+"'"

                insertquery = "INSERT INTO studios (studioname, company, city, country, foundeddate, enddate) VALUES ("+intext[0].replace("\"","\'")+","+intext[1].replace("\"","\'")+","+intext[2].replace("\"","\'")+","+intext[3].replace("\"","\'")+","+intext[4].replace("\"","\'")+","+intext[5].replace("\"","\'")+")"
                cur.execute(insertquery)
                conn.commit()
            f.close()
            print("studios done")

    def insertAwards(cur,conn):
        createAw = """CREATE TABLE awardstype
(
    award varchar(20) NOT NULL,
    organization varchar(200),
    country varchar(3) references geography (code),
    colloquial varchar(100),
    year smallint,
    notes varchar(100),
    CONSTRAINT awardstype_pkey PRIMARY KEY (award)
);"""
        cur.execute(createAw)
        awards = [["'AA'", "'Hollywood Academy of Motion Picture Arts and Sciences'", "'Am'", "'Oscar'", "NULL", "NULL"],
                  ["'AAN'", "'Hollywood Academy of Motion Picture Arts and Sciences'", "'Am'", "'Oscar nomination'", 'NULL','NULL'],
                  ["'AFI Lifetime'", "'American Film Institute'", "'Am'", "'annual awards since 1973'",'NULL','NULL'],
                  ["'AFI77'", "'American Film Institute'", "'Am'", "'Best movies poll'", '1977','NULL'],
                  ["'Baer'", "'Berlinale'", "'Ge'", "'Berliner Baer(-Gold,Silver,Bronze)'", '1951','NULL'],
                  ["'BFA'", "'British Film Academy'", "'GB'", "'Stella'",'NULL','NULL'],
                  ["'CC'", "'Siena Research Institute, for the Centennial Committee of the Hollywood Chamber of Commerce, with Siena College, Loudonville NY'", "'Am'", 'NULL','1987','NULL'],
                  ["'Crystal Heart'", "'Heartland Film Festival'",'NULL','NULL', '1991','NULL'],
                  ["'Delluc'", "'Le Prix Louis-Delluc'", "'Fr'", 'NULL', 'NULL', 'NULL'],
                  ["'aw'", "'Award Unknown'", 'NULL', 'NULL', 'NULL', 'NULL'],
                  ["'Emmy'", "'TV Acdemy'", "'Am'", "'Emmy'", 'NULL', 'NULL'],
                  ["'Fnn'", "'Entertainment Weekly'", "'Am'", 'NULL', 'NULL', 'NULL'],
                  ["'Felix'", "'European Film Festival'", "'Br'", 'NULL', '1988', 'NULL'],
                  ["'Genie'", "'Canadian Academy'", "'Ca'",'NULL', '1991','NULL'],
                  ["'H****'", "'Halliwells Film Guide'", "'GB'","'four stars'", '1983','NULL'],
                  ["'H***'", "'Halliwells Film Guide'", "'GB'","'three stars'", '1983','NULL'],
                  ["'H**'", "'Halliwells Film Guide'", "'GB'","'two stars'", '1983','NULL'],
                  ["'H*'", "'Halliwells Film Guide'", "'GB'","'one star'", '1983','NULL'],
                  ["'H'", "'Halliwells Film Guide'", "'GB'","'cited'", '1983','NULL'],
                  ["'Hersholt'", "'Academy'", "'Am'", "'humanitarian'", '1983','NULL'],
                  ["'JE'", "'John Eastman: 500 Retakes'", "'Am'",'NULL','1985','NULL'],
                  ["'LAA'", "'American Film Institute'", "'Am'", "'Life Achievement Award'",'NULL','NULL'],
                  ["'MMA'", "'Museum of Modern Art'", "'Am'", "'Film Festival'", 'NULL', 'NULL'],
                  ["'NBR'", "'National Board of Reviews'", "'Am'",'NULL','NULL','NULL'],
                  ["'NFR'", "'National Film Registry'", "'Am'", "'Library of Congress'", '1992', "'Nt(Public Law 102-307) Nt(100 films as of 1992)'"],
                  ["'NYFCC'", "'New York Film Critics Circle'","'Am'",'NULL','NULL','NULL'],
                  ["'NSFC'", "'National Society of Film Critics'", "'Am'",'NULL', '1965','NULL'],
                  ["'RFP'", "'Cinema Trade Benevolent Organization'", "'GB'", "'Royal Film Performance'", '1946', 'NULL'],
                  ["'Palm'", "'Cannes Film Festival'","'It'", "'Golden Palm'", 'NULL','NULL'],
                  ["'SFIFF'", "'San Francisco International Film Festival'","'Am'", 'NULL','NULL','NULL'],
                  ["'TMA'", "'Hollywood Academy of Motion Picture Arts and Sciences'", "'Am'", "'Thalberg Memorial Award'", 'NULL','NULL'],
                  ["'Tony'","'Antoinette Perry Award'", "'Am'", "'Tony'",'NULL',"'Nt(TV)'"],
                  ["'T90'", "'Time Magazine'", "'Am'", "'Movies of the dcecade'",'NULL','NULL'],
                  ["'VFF'", "'Venice Film Festival'", "'It'", "'Venice'", 'NULL', 'NULL'],
                  ["'WAMPAS'", "'Western Association of Motion Picture Advertisers'", "'Am'", "'WAMPAS promising actress 1922-1934'", '1922', 'NULL'],
                  ["'Z*'", "'Fred Zinneman'",'NULL', "'book'",'NULL','NULL']]
        for i in awards:
            insertquery="INSERT INTO awardstype (award, organization, country, colloquial, year, notes) VALUES("+i[0]+","+i[1]+","+i[2]+","+i[3]+","+i[4]+","+i[5]+");"
            #print(insertquery)
            cur.execute(insertquery)
            conn.commit()
        print("Awards done")

                    

    # def insertPeoplecode(cur,conn):
    #     codes=[('D','Director'),('P','Producer'),('W','Writer'),('B','Book Author'),
    #            ('C','Cinematographer'),('CoD',	'CoDirector'),('Chor',	'choreographer'),('Gn',	'Female Producer or Director'),
    #            ('M', 'composer'),('S','Sound Engineer'), ('X','Unknown'), ('A','Auditor'), ('G','Gaffer'), ('V',	'Visual art director'),('R',	'Visual art director'), ('E', 'Editor')]
    #     for j in codes:
    #         insertquery="INSERT INTO peoplecode (code, description) VALUES('"+j[0]+"','"+j[1]+"');"
    #         cur.execute(insertquery)
    #         conn.commit()

    def insertRoletypes(cur,conn):
        createRoletype = """CREATE TABLE roletypes
                (
                    roletype varchar(10) NOT NULL,
                    description varchar(50),
                    CONSTRAINT roletypes_pkey PRIMARY KEY (roletype)
                );
                """
        cur.execute(createRoletype)
        string="""<tr> <td> \Adv<td> adversary<td> |  <tr> <td> \Agn<td> agent<td> | <tr> <td> \Ani<td> animal<td> |
<tr> <td> \Bit<td> bit role<td> |
<tr> <td> \Cam<td> cameo role<td> |  <tr> <td> \Cro<td> crook<td> |
<tr> <td> \Grp<td> group or band<td> |
<tr> <td> \Her<td> hero<td> |
<tr> <td> \Inn<td> innocent<td> |
<tr> <td> \Lov<td> love interest<td> |
<tr> <td> \Sav<td> savior<td> |  <tr> <td> \Sci<td> scientist<td> | <tr> <td> \Sdk<td> sidekick<td> |
<tr> <td> \Sus<td> suspect<td> |
<tr> <td> \Rul<td> ruler<td> |
<tr> <td> \Psy<td> psychopath<td> |
<tr> <td> /Und<td> undetermined<td> |
<tr> <td> \Vmp<td> vamp<td> |  <tr> <td> \Vic<td> victim<td> | <tr> <td> \Vil<td> villain}<td> |
<tr> <td> \Voi<td> voice only, narrator<td> |
<tr> <td> \Wmp<td> wimp<td> |"""
        text=string.split('<tr>')
        text.pop(0)
        for i in text:
            j=i.strip().split('<td>')
            insertquery="INSERT INTO roletypes (roletype, description) VALUES('"+j[1][2:]+"','"+j[2]+"');"
            cur.execute(insertquery)
            conn.commit()

    def insertColorcodes(cur,conn):
        createCol = """CREATE TABLE colorcodes
(
    code varchar(10) NOT NULL,
    fullname varchar(50) NOT NULL,
    description varchar(100),
    CONSTRAINT colorcodes_pkey PRIMARY KEY (code)
);"""
        cur.execute(createCol)
        string="""prc	unknown		|
                col	color	color film, common after 1955	|
                bnw	black-and-white	b-w film common before 1945	|
                sbw	silent	silent black-and-white film	|
                cld	colored	black-and-white film recolored	|
                Cart	cartoon	Cartoons are normally colored	|
                Tcol	Technicolor	high quality color	|
                Ecol	Eastmancolor	color by Kodak		|
                Wcol	Warnercolor		|
                Mcol	Metrocolor	Color by MGM	|
                Acol	Anscocolor	color by Kodak	|
                Agcol	Agfacolor		|
                Fcol	Fujicolor		|
                DeLuxe	DeLuxe	low cost color	|
                DuArt	DuArt	color	|
                Movielab	MovieLab	color	|
                CS	Cinemascope	widescreen, mostly color	|
                Trama	Technirama	widescreen color	|
                Pan	PanaVision		|
                TV	film made for TV	various processes	|
                Vst	Vistavision		|"""
        text=string.split('\n')
        for i in text:
            j=i.strip().split('\t')
            if len(j[2])>0:
                j[2]="'"+j[2]+"'"
            else:
                j[2]='NULL'
            insertquery="INSERT INTO colorcodes (code, fullname, description) values ('"+j[0]+"','"+j[1]+"',"+j[2]+");"
            cur.execute(insertquery)
            conn.commit()
        print("Colorcodes done")

    def insertCategories(cur,conn):
        createCat = """CREATE TABLE categories
(
    code varchar(5) NOT NULL,
    category varchar(50) NOT NULL,
    CONSTRAINT categories_pkey PRIMARY KEY (code)
);"""
        cur.execute(createCat)
        string = """Susp	thriller	|
                    CnR	cops and robbers	|
                    Dram	drama	|
                    West	western	|
                    Myst	mystery	|
                    S.F.	science fiction	|
                    Advt	adventure	|
                    Horr	horror	|
                    Romt	romantic	|
                    Comd	comedy	|
                    Musc	musical	|
                    Docu	documentary	|
                    Porn	pornography, including soft	|
                    Noir	black	|
                    BioP	biographical Picture	|
                    TV	TV show	|
                    TVs	TV series	|
                    TVm	TV miniseries	| 
                    Ctxx	uncategorized	|
                    Actn	violence	|	
                    AvGa	Avant Garde	|
                    Camp	now - camp	|	
                    Cart	cartoon	|
                    Disa	Disaster	|
                    Epic	epic	|
                    Faml	family	|	
                    Hist	history	|
                    ScFi	science fiction	|	
                    Surl	sureal	|
                    Fant\tFantasy\t|"""
        text=string.split('\n')
        for i in text:
            j=i.strip().split('\t')
            insertquery="insert into categories (code,category) values ('"+j[0]+"','"+j[1]+"');"
            cur.execute(insertquery)
            conn.commit()
        print("Categoies done")

    def insertGeography(cur,conn):
        creategeo = """CREATE TABLE geography
(
    code varchar(3) NOT NULL,
    country varchar(50) NOT NULL,
    adjective varchar(50),
    CONSTRAINT geography_pkey PRIMARY KEY (code)
);"""
        cur.execute(creategeo)
        string="""Am	USA	American	|
                Br	Great Britain	British	|	
                GB	Great Britain	British	|
                Fr	France	French	|
                Ge	Germany	German	|
                It	Italy	Italian	|
                Ja	Japan	Japanese	|
                Ar	Argentinia	Argentine	|
                Au	Australia	Australian	|
                Be	Belgium	Belgian	|
                Bz	Brazil	Brazilian	|
                Ca	Canada	Canadian	|
                Ch	China	Chinese	|
                Cz	Czechoslovakia	Czech	|
                Da	Denmark	Danish	|	
                Gr	Greece	Greek	|	
                Du	Holland	Dutch	|	
                Hu	Hungary	Hungarian	|
                In	India	Indian	|
                Ir	Ireland	Irish	|
                Me	Mexico	Mexican	|
                Os	Austria	Austrian	|
                Pe	Peru	Peruvian	|	
                Ru	Russia	Russian	|
                Sp	Spain	Spanish	|
                SA	South-Africa	South-African	|
                Yu	Yugoslavia	Yugoslav	|
                Zw	Switzerland	Swiss	|
                Cu\tCuba\tCuban\t|
                Po\tPortugal\tPostugese\t|
                WI\tWest-India\tWest-Indians\t|
                Tu\tTurkey\tTurkish\t|
                Sw\tSwitzerland\tSwiss\t|
                Ct\tCentral-Afraica\tAfrican"""
        
        text=string.split('\n')
        for i in text:
            j=i.strip().split('\t')
            insertquery="insert into geography (code,country,adjective) values ('"+j[0]+"','"+j[1]+"','"+j[2]+"');"
            cur.execute(insertquery)
            conn.commit()
        print("Geograpy Done")

    def insertCasts(cur,conn):
        createcasts= """CREATE TABLE casts
                (
                    film_id varchar(20),
                    title varchar(100),
                    actor varchar(100),
                    roletype varchar(20),
                    role varchar(100),
                    CONSTRAINT casts_actor_fkey FOREIGN KEY (actor)
                        REFERENCES public.actors (stagename) MATCH SIMPLE
                        ON UPDATE CASCADE
                        ON DELETE CASCADE,
                    CONSTRAINT casts_film_id_fkey FOREIGN KEY (film_id)
                        REFERENCES public.movies (film_id) MATCH SIMPLE
                        ON UPDATE CASCADE
                        ON DELETE CASCADE,
                    CONSTRAINT casts_roletype_fkey FOREIGN KEY (roletype)
                        REFERENCES public.roletypes (roletype) MATCH SIMPLE
                        ON UPDATE CASCADE
                        ON DELETE CASCADE
                );"""
        cur.execute(createcasts)
        with open('casts.csv','r') as f:
            for line in f:
                l = line.split('\n')[0]
                l=l.split(';')
                for i in range(len(l)):
                    l[i] = l[i][1:-1]
                if ':' in l[4]:
                    l[4] = l[4].split(':')[1]
                lquery = f"INSERT INTO casts (film_id, title, actor, roletype, role) VALUES ('{l[0]}', '{l[1]}','{l[2]}','{l[3]}','{l[4]}')"
                try:
                    cur.execute(lquery)
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    print(e)