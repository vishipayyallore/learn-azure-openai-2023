from flask import Flask
from dotenv import dotenv_values
from api_routes import api_routes_bp
from logging_config import configure_logging
from db_config import db


def create_app():
    app = Flask(__name__)

    # Load configuration from .env file
    config_details = dotenv_values(".env")
    app.config['SQLALCHEMY_DATABASE_URI'] = config_details['SQLSERVERCONNECTIONSTRING']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_details['SQLALCHEMY_TRACK_MODIFICATIONS']

    # Configure the app's logging settings
    configure_logging(app)

    # Initialize the SQLAlchemy database
    db.init_app(app)

    # Register the API routes blueprint
    app.register_blueprint(api_routes_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
