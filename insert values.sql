INSERT INTO roletypes (roletype, description) 
VALUES 	('Adv','adversary'),
		('Agn','agent'),
		('Ani','animal'),
		('Bit','bit role'),
		('Cam','cameo role'),
		('Cro',	'crook'),
		('Grp','group or band'),
		('Sci'	,'scientist'),
		('Inn',	'innocent'),
		('Und'	,'undetermined');
		
INSERT INTO colorcodes (code, fullname, description)
Values	('prc','unknown',NULL),
		('col',	'color','color film, common after 1955'),
		('bnw',	'black-and-white','b-w film common before 1945'),
		('sbw','silent','silent black-and-white film'),
		('cld',	'colored',	'black-and-white film recolored'),
		('Cart',	'cartoon',	'Cartoons are normally colored');
		
INSERT INTO categories (code,category)
Values ('Susp',	'thriller'),
		('CnR',	'cops and robbers'),
		('Dram',	'drama'),
		('West',	'western'),
		('Myst',	'mystery'),
		('Comd', 'Comedy'),
		('Ctxx',	'uncategorized');
		
INSERT INTO peoplecode (code, description)
Values ('D', 'Director'),
		('P', 'Producer'),
		('W', 'Writer');
		
INSERT INTO geography (code, country, adjective)
Values ('Am',	'USA',	'American'),
		('Br',	'not used',	'British'),
		('GB',	'Great Britain',	'not used'),
		('Fr',	'France',	'French'),
		('Ge',	'Germany',	'German'),
		('It',	'Italy',	'Italian'),
		('Ja',	'Japan',	'Japanese'),
		('Hu',	'Hungary',	'Hungarian'),
		('Au',	'Australia',	'Australian');

INSERT INTO awardstype (award, organization, country, colloquial, year, notes)
VALUES ('AA',	'Hollywood Academy of Motion Picture Arts and Sciences',	'USA',	'Oscar', NULL,NULL),
		('AAN',	'Hollywood Academy of Motion Picture Arts and Sciences',	'USA',	'Oscar nomination',NULL,NULL),
		('AFI Lifetime',	'American Film Institute',	'USA',	'annual awards since 1973', 1973,NULL),
		('AFI77',	'American Film Institute',	'USA',	'Best movies poll', 1977,NULL),
		('Baer',	'Berlinale',	'Germany',	'Berliner Baer(-Gold,Silver,Bronze)',	1951,NULL),
		('H****','Halliwell`s Film Guide',	'Great Britain',	'four stars',	1983,NULL),
		('H***','Halliwell`s Film Guide',	'Great Britain',	'three stars',	1983,NULL);
		
		
INSERT INTO people (ref_name, d_id, years, last_name, first_name, yob, yodeath,country)
VALUES 	('Aaron',	'D',	'PAa', '1979',	'Aaron',	'Paul', NULL,NULL,'Am'),
		('Abel',	'D',	'JeA','1971',	'Abel',	'Jeanne',NULL,NULL,'Am'),
		('Abbott','D','GgA','1929-1958',	'Abbott',	'George','1887',NULL,'Am'),
		('Abrahams',	'D','xAb',	'1948',	'Abrahams',NULL,NULL,NULL,'Am'),
		('J.Abrahams',	'D',	'JiA'	,'1980-1988',	'Abrahams',	'Jim',NULL,NULL,'Am'),
		('Asquith',	'D',	'AA',	'1928',	'Asquith',	'Anthony `Puffin',	1902,	1968	,'Br'),
		('G.Pascal',	'P',	'GPa',	'1940-1945',	'Pascal'	,'Gabriel',	1894,	1954,	'Hu'),
		('David Kelly'	,'P',	NULL,	1993,	'Kelly'	,'David E.',	1956,NULL,	'Am');
		
INSERT INTO studios (studioname, company, city, country, foundeddate, enddate)
VALUES ('Projection-Praxinoscope',NULL,NULL,'France','1881','1882'),
		('Film Camera',NULL,NULL,'Germany','1889',NULL),
		('35mm Film Camera',	'Edison',	'New Jersey','USA',	'1893',NULL),
		('Kinetoscope',	'Edison','New Jersey','USA',	'1894',NULL),
		('Practical Projectors',	'Lumiere Fr.','Lyon',	'France',	'1895',NULL),
		('Paramount',	'Paramount Corp.','Los Angeles',	'USA',	'1916',	'1993');
		
INSERT INTO actors (stagename, yearsinwork, lastname, firstname, gender, yob, yod, roles, country)
VALUES ('Willie Aames',NULL,'Aames',	'William',	'M',	'1960',	'199x',	NULL,'Am'),
		('Bud Abbott',	'1939-1956',	'Abbott',	'William',	'M',	'1895',	'1974',	'straight, comedian','Am'),
		('Diahnne Abbott','1976-1982',NULL,NULL,'F',NULL,'199x','sexy','Am'),
		('Leslie Howard',	'1930-1943',	'Stainer',	'Leslie'	,'M'	,1890,	1943,	'romantic intellectual',	'Hu'),
		('George Abbott',	'1928-1958',	'Abbott',	'George',	'M',	'1887',	'199x',	'playwright, producer','Am'),
		('Wendy Hiller',	'1937-1982',	'Hiller',	'Wendy',	'F',	1912,	'199x',	'distinguished, inimitable voice','Br'),
		('Marie Lohr',	'1932-1956',	'Lohr',	'Marie',	'F',	1890,	1975,	'distinguished',	'Au')
		('Wilfrid Lawson'	,'1936-1966',	'Worsnop'	,'Wilfrid'	,'M'	,1900,	1966,	'character'	,'Br');

INSERT INTO movies (film_id, title, release_year, director, producers, studios, process, category, awards) 
VALUES ('AA13',	'Pygmalion'	,1938,	'Asquith'	,'G.Pascal',NULL	,	'bnw',	'Comd',	'H****'),
		 ('AA14','French Without Tears',	1939,	'Asquith','David Kelly'	,'Paramount'	,'bnw',	'Ctxx',	NULL),
		 ('AA16','Quiet Wedding',	1940,	'Asquith',	NULL	,'Paramount','bnw',NULL,'H***'),
		 ('AA20','The Demi-Paradise',	1943,	'Asquith',NULL,NULL,'prc',	'Ctxx',NULL),
		 ('LuB20','Pygmalion',1937,	'Aaron','David Kelly','Kinetoscope','bnw','Dram','AA'),
		('HH15','Twentieth Century',	1934,'Aaron','David Kelly','Paramount','bnw',	'Comd'	,'H****');

	

INSERT INTO casts (film_id, title, actor, roletype, role) 
VALUES ('AA13','Pygmalion',	'Leslie Howard',	'Sci','smug professor \"Higgins\"'),
		 ('AA13','Pygmalion',	'Wendy Hiller',	'Inn',	'flower girl \"Eliza\"'),
		 ('AA13','Pygmalion',	'Wilfrid Lawson'	,'Und',	'friend \"Dolittle\"'),
		 ('AA13',	'Pygmalion',	'Marie Lohr',	'Und',	'wife \"Mrs.Higgins\"');


INSERT INTO public.movies_director(
	film_id, director)
	Select film_id,director from movies;

INSERT INTO public.movies_director(
	film_id, producers)
	Select film_id,producers from movies;
	
INSERT INTO public.movies_normalized(
	film_id, title, release_year, studios, process, category, awards)
	SELECT film_id, title, release_year,studios,process,category,awards from movies;

