# -*- coding: utf-8 -*-
import functools

from flask import Blueprint  # Blueprint - это что-то наподобие приложения, которое отвечает за свою часть функций
from flask import request  # глобальный объект запроса
from flask import redirect # функция перенаправления
from flask import url_for # функция создающая url
from flask import flash
from flask import render_template # шорткат для рендера шаблона
from flask import session # объект сессии
from flask import g

# импортируем функции хэширования пароли и проверки хэша
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import username_exist, add_user, get_user_by_name, get_user_by_id


# Создаем блюпринт для целей аутентификации и привязываем url_prefix
# теперь с помощью bp мы может например задавать роуты и прочее, как примерно мы делали с приложением
bp = Blueprint("auth", __name__, url_prefix="/auth")


# теперь прописываем view functions
@bp.route("/register", methods=("GET", "POST"))
def register():

    # Если POST то проверяем и добавляем пользователя
    if request.method == "POST":
        # Вытаскиваем поля формы из реквеста
        username = request.form["username"]
        password = request.form["password"]

        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"
        elif username_exist(username):
            error = "user {} already exists" % (username,)

        if error is None:
            add_user(username, generate_password_hash(password))
            return redirect(url_for("auth.login"))

        flash(error)

    # если же get, то выдаем страницу регистрации
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        user = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"

        if error is None:
            user = get_user_by_name(username)

            if user is None:
                error = "Incorrect username"
            elif not check_password_hash(user["password"], password):
                error = "Incorrect password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    redirect(url_for("index"))

# Создадим функцию выполняющуюся перед каждым запросом и получающим из сессии полноценного пользователя
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user  = None
    else:
        g.user = get_user_by_id(user_id)


# Декоратор для view по которым нужно проверять авторизацию
def login_reqired(view):
    @functools.wraps(view)
    def wrapped(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped
