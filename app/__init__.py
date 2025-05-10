import os
from flask import Flask


def create_app():
    """Фабрика для создания Flask-приложения.

    Настраивает:
    - Пути к шаблонам и статике
    - Секретный ключ
    - Регистрацию blueprint'ов

    Returns:
        Flask: Сконфигурированное приложение
    """
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
        static_folder=os.path.join(os.path.dirname(__file__), 'static')
    )
    app.secret_key = 'your_secret_key'

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app