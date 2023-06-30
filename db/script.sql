create table users
(
    id         integer primary key,
    nom        varchar(100),
    typeCompte integer,
    courriel   varchar(100),
    hache      varchar(32),
    salt       varchar(128)
);

CREATE TABLE Events
(
    event_id         INTEGER PRIMARY KEY,
    creator_id       INTEGER,
    title            TEXT NOT NULL,
    start_date_time  TEXT NOT NULL,
    end_date_time    TEXT NOT NULL,
    location         TEXT NOT NULL,
    flyer_image      BLOB,
    description      TEXT,
    max_registration INTEGER,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

