from env_config import get_config_value
from flask import Flask
from api_routes import api_routes_bp
from logging_config import configure_logging
from db_config import db


def create_app():
    app = Flask(__name__)

    # Load configuration from .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = get_config_value(
        "SQLSERVERCONNECTIONSTRING")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = get_config_value(
        'SQLALCHEMY_TRACK_MODIFICATIONS')

    # Configure the app's logging settings
    configure_logging(app)

    # Initialize the SQLAlchemy database
    db.init_app(app)

    # Register the API routes blueprint
    app.register_blueprint(api_routes_bp)

    return app
