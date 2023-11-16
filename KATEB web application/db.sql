CREATE TABLE users (
    id INTEGER,
    Fname TEXT NOT NULL,
    Lname TEXT NOT NULL,
    username TEXT NOT NULL,
    passwort TEXT NOT NULL,
    -- cash NUMERIC NOT NULL DEFAULT 10000.00,
    PRIMARY KEY(id)
);

INSERT INTO users (username, passwort, Fname, Lname) VALUES ('test', 'test', 'Iman', 'Aghaei');

CREATE UNIQUE INDEX username ON users (username);


CREATE TABLE father (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    pipname TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE UNIQUE INDEX pipname ON father (pipname);

CREATE TABLE mother (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 mother_id INTEGER NOT NULL,
 user_id INTEGER NOT NULL,
 pipname TEXT NOT NULL,
 mother_month INTEGER NOT NULL,
 mother_year NUMERIC NOT NULL,
 time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(mother_id) REFERENCES father(id),
 FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE kid (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 kid_id INTEGER NOT NULL,
 user_id INTEGER NOT NULL,
 station REAL NOT NULL,
--  potential INTEGER NOT NULL,
 consideration  TEXT NOT NULL,
--  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--  FOREIGN KEY(kid_id) REFERENCES father(id),
 FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE baby (
 id_check INTEGER PRIMARY KEY AUTOINCREMENT,
 id INTEGER,
 baby_id INTEGER,
 user_id INTEGER,
 baby_station REAL NOT NULL,
--  address_name TEXT,
 potential INTEGER NOT NULL,
 consideration  TEXT,
 date DATE DEFAULT CURRENT_DATE,
 time TIME DEFAULT CURRENT_TIME,
--  FOREIGN KEY(baby_id) REFERENCES kid(kid_id),
 FOREIGN KEY(user_id) REFERENCES users(id)
);


