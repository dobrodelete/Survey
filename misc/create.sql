-- we don't know how to generate root <with-no-name> (class Root) :(
create table admins
(
    id INTEGER primary key autoincrement,
    name TEXT not null unique,
    password TEXT not null
);

create table users
(
    id INTEGER primary key autoincrement,
    post TEXT not null,
    iogv_id TEXT REFERENCES iogv,
    subdivision_id TEXT REFERENCES iogv,
    person_id TEXT,
    created_at TEXT not null
);

CREATE TABLE iogv (
    hierarchy_id TEXT PRIMARY KEY,
    depth_level INTEGER NOT NULL,
    name TEXT NOT NULL,
    parent_id TEXT REFERENCES iogv
);

create table record
(
    id INTEGER primary key autoincrement,
    uid INTEGER references users,
    responce_time TEXT,
    created_at TEXT not null
);

create table answers
(
    rid INTEGER references record,
    number_question INTEGER NOT NULL,
    answer REAL NOT NULL,
    comment TEXT
);