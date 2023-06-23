create table users(
    id integer primary key,
    nom varchar(50),
    typeCompte integer,
    courriel varchar(100),
    hache varchar(32),
    salt varchar(128)
);
