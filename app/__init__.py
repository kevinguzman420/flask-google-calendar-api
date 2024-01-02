from flask import Flask


def create_app(settings_module):
    app = Flask(__name__)
    app.config.from_object(settings_module)

    from app.main.views import main_bp

    app.register_blueprint(main_bp)

    return app
