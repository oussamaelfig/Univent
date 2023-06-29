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
    event_id        INTEGER PRIMARY KEY,
    creator_id      INTEGER,
    title           TEXT NOT NULL,
    start_date_time TEXT NOT NULL,
    end_date_time   TEXT NOT NULL,
    location        TEXT NOT NULL,
    flyer_image     BLOB,
    description     TEXT,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

CREATE TABLE Tickets
(
    ticket_id                INTEGER PRIMARY KEY,
    event_id                 INTEGER,
    ticket_name              TEXT    NOT NULL,
    ticket_type              TEXT    NOT NULL,
    price                    REAL    NOT NULL,
    available_tickets        INTEGER NOT NULL,
    ticket_description       TEXT,
    sales_start_date         TEXT    NOT NULL,
    sales_end_date           TEXT    NOT NULL,
    min_tickets_per_purchase INTEGER NOT NULL,
    max_tickets_per_purchase INTEGER NOT NULL,
    FOREIGN KEY (event_id) REFERENCES Events (event_id)
);
