DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password text not null
);

create table post(
    id integer primary key autoincrement,
    author_id integer not null,
    created timestamp not null default current_timestamp,
    title text not null,
    body text not null,
    foreign key (author_id) references user (id)
);

