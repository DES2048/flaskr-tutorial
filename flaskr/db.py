# -*- coding: utf-8 -*-
import sqlite3

from flask import g  # глобальный объект, в котором хранится вся информация в течении обрабоки запроса
from flask import current_app # ссылка на созданое приложение, чтобы не передаватькуда угодно созданное нами
# приложение

import click # импортим модуль для создания cli
from flask.cli import with_appcontext


# иниц. наш db модуль, подключая закрытие бд после обработки запроса
# и подключаем нашу команду к flask.cli
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# Первоначальная инициализация нашей бд
def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


# Создает подключение и помещает его в g, если его там еще нет,
# возвращает созданное подключение
def get_db():
    if "db" not in g:
        # берем путь к бд из конфига нашего приложения и созд. подключение
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


# добавим свою команду в flask cli
@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Database initializated")

# db helper functions


# checking if user with given username exists
def username_exist(username):
    db = get_db()

    return db.execute(
        "select id from user where username = ?", (username,)
    ).fetchone() is not None


def add_user(username, password):
    db = get_db()

    db.execute("insert into user(username, password) values (?, ?)", (username, password))
    db.commit()


def get_user_by_name(username):
    db = get_db()

    user = db.execute("select * from user where username = ?", (username,)).fetchone()

    return user


def get_user_by_id(id):
    db = get_db()

    user = db.execute("select * from user where id = ?", (id,)).fetchone()

    return user


def get_posts_all():
    db = get_db()

    posts = db.execute(
        "select p.id, title, body, created, author_id, username"
        " from post p join user u ON p.author_id = u.id"
        " order by created desc"
    ).fetchall()

    return posts


def add_post(author_id, title, body):
    db = get_db()

    db.execute(
        "insert into post(author_id, title, body) values(?, ?, ?)",
        (author_id, title, body)
    )

    db.commit()


def get_post_by_id(id):
    db = get_db()

    post = db.execute(
        "select p.id, title, body, created, author_id, username"
        " from post p join user u ON p.author_id = u.id"
        " where p.id = ?"
        " order by created desc", (id,)
    ).fetchone()

    return post


def update_post(post_id, title, body):
    db = get_db()
    db.execute(
        'UPDATE post SET title = ?, body = ?'
        ' WHERE id = ?',
        (title, body, post_id)
    )
    db.commit()
