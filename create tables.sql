CREATE TABLE roletypes
(
    roletype varchar(10) NOT NULL,
    description varchar(50),
    CONSTRAINT roletypes_pkey PRIMARY KEY (roletype)
);

CREATE TABLE colorcodes
(
    code varchar(10) NOT NULL,
    fullname varchar(50) NOT NULL,
    description varchar(100),
    CONSTRAINT colorcodes_pkey PRIMARY KEY (code)
);

CREATE TABLE categories
(
    code varchar(5) NOT NULL,
    category varchar(50) NOT NULL,
    CONSTRAINT categories_pkey PRIMARY KEY (code)
);

CREATE TABLE geography
(
    code varchar(3) NOT NULL,
    country varchar(50) NOT NULL,
    adjective varchar(50),
    CONSTRAINT geography_pkey PRIMARY KEY (code)
);

CREATE TABLE studios
(
    studioname varchar(50) NOT NULL,
    company varchar(100),
    city varchar(50),
    country varchar(50) references geography (code),
    foundeddate varchar(20),
    enddate varchar(20),
    CONSTRAINT studios_pkey PRIMARY KEY (studioname)
);


CREATE TABLE people
(
    ref_name varchar(50) NOT NULL,
    d_id varchar(10),
    years varchar(50),
    last_name varchar(50),
    first_name varchar(50),
    yob varchar(5),
    yodeath varchar(5),
    CONSTRAINT people_pkey PRIMARY KEY (ref_name)
);

CREATE TABLE awardstype
(
    award varchar(20) NOT NULL,
    organization varchar(200),
    country varchar(3) references geography (code),
    colloquial varchar(100),
    year smallint,
    notes varchar(100),
    CONSTRAINT awardstype_pkey PRIMARY KEY (award)
);



CREATE TABLE actors
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
);

CREATE TABLE movies
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
);

CREATE TABLE casts
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
);

CREATE TABLE movies_normalized(
    film_id varchar(20) NOT NULL,
    title varchar(200) NOT NULL,
    release_year varchar(5),
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
    CONSTRAINT movies_process_fkey FOREIGN KEY (process)
        REFERENCES public.colorcodes (code) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT movies_studios_fkey FOREIGN KEY (studios)
        REFERENCES public.studios (studioname) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE movies_director(
    film_id varchar(20) NOT NULL,
    director varchar(100),
    CONSTRAINT movies_pkey PRIMARY KEY (film_id),
    CONSTRAINT movies_director_fkey FOREIGN KEY (director)
        REFERENCES public.people (ref_name) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE

);

CREATE TABLE movies_producer(
    film_id varchar(20) NOT NULL,
    producers varchar(100),
    CONSTRAINT movies_pkey PRIMARY KEY (film_id),
    CONSTRAINT movies_producers_fkey FOREIGN KEY (producers)
        REFERENCES public.people (ref_name) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE

);