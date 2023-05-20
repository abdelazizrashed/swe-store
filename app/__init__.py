
import uuid

from flask import Flask

from flask_session import Session

from .api import register_routes


def create_app():
    app = Flask(__name__, template_folder='website/templates',
                static_folder='website/static')

    from .website.view import create_app as website_create_app

    app.register_blueprint(website_create_app())


# set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.secret_key = str(uuid.uuid4())
    app.config['SESSION_TYPE'] = 'filesystem'

    app.config.from_object(__name__)
    Session(app)

    register_routes(app)

    return app
