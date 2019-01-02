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
