from flask import Flask
from dotenv import dotenv_values
from api.api_routes import api_routes_bp
from utils.logging_config import configure_logging
from utils.db_config import db
from urllib.parse import quote_plus  # Import the quote_plus function

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to Python Flask API!'

def create_app():

    # Load configuration from .env file
    config_details = dotenv_values(".env")

    connection_string = config_details["SQLSERVERCONNECTIONSTRING"]

    # Configure the SQLAlchemy database
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_details['SQLALCHEMY_TRACK_MODIFICATIONS']

    # Configure the app's logging settings
    configure_logging(app)

    # Initialize the SQLAlchemy database
    db.init_app(app)

    # Register the API routes blueprint
    app.register_blueprint(api_routes_bp, url_prefix='/api')

    return app


# Create the app and run it during development
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # During development

# # For production deployment, comment out the above lines and use the one below
# app = create_app()
# app.run()  # In production