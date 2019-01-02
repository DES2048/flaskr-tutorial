# coding=utf-8
import os

from flask import Flask  # Импортиуем класс Flask, инстанс которого и будет нашим приложением


# Эта функция, т.н application factory в ней создается и настравивается наше приложение
def create_app(test_config=None):

    # Создаем инстанс нашего приложения и указываем что мы будем использовать относительные пути
    # для поиска  конфигурации для нашего приложения
    app = Flask(__name__, instance_relative_config=True)

    # config - что то типа словаря с настройками нашего приложения
    # при запуске flask создает папку instance и поэтому путь к бд мы указываем относительно этой директории
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    # выбираем способ настройки придложения в зависимости от того
    # передали мы test_config или нет
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # flask не создает автоматически instance folder, поэтому мы сделаем это сами
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # настраиваем модуль db
    from . import db
    db.init_app(app)

    # регаем blueprints
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    # Ну и созадим простой view И прицепим к нему роут
    @app.route("/hello")
    def hello():
        return "Hello from Flask App!"

    # Ну и возвращаем наше приложение
    return app

