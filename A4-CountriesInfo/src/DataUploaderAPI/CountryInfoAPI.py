import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values
import pyodbc
from urllib.parse import quote_plus  # Import the quote_plus function

app = Flask(__name__)

# Load configuration from .env file
config_details = dotenv_values(".env")

# Encode the password using quote_plus
encoded_password = quote_plus(config_details['PASSWORD'])

# # Construct the SQLAlchemy database URI with the encoded password
# db_uri = f"mssql+pyodbc://{config_details['USERNAME']}:{encoded_password}" \
#          f"@{config_details['SERVER']},{config_details['PORT']};" \
#          f"DATABASE={config_details['DATABASE']};" \
#          f"DRIVER={config_details['DRIVER']}"

# # Construct the SQLAlchemy database URI without the DSN
# db_uri = f"mssql+pyodbc://{config_details['USERNAME']}:{encoded_password}" \
#          f"@{config_details['SERVER']},{config_details['PORT']};" \
#          f"DATABASE={config_details['DATABASE']};" \
#          f"DRIVER={{{config_details['DRIVER']}}}"
# print(db_uri)

# Construct the connection string
# connection_string = f"Driver={{{config_details['DRIVER']}}};Server=tcp:{config_details['SERVER']},{config_details['PORT']};" \
#                     f"Database={config_details['DATABASE']};Uid={config_details['USERNAME']};" \
#                     f"Pwd={config_details['PASSWORD']};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"


connection_string = config_details["SQLSERVERCONNECTIONSTRING"]
# Print the connection string
print(connection_string)

# Configure the SQLAlchemy database
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={pyodbc.connect(connection_string)}"
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"

# Configure the SQLAlchemy database
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_details['SQLALCHEMY_TRACK_MODIFICATIONS']
db = SQLAlchemy(app)

# Configure app-wide logging settings
app.logger.setLevel(logging.DEBUG)  # Set the log level to DEBUG

# Create a file handler to write logs to a file
file_handler = logging.FileHandler('app.log')
# Set the log level for the file handler to DEBUG
file_handler.setLevel(logging.DEBUG)

# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)  # Set the formatter for the file handler

# Add the file handler to the Flask app's logger
app.logger.addHandler(file_handler)


class CountryInfo(db.Model):
    __tablename__ = 'CountryInfo'
    CountryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CountryName = db.Column(db.String(100))
    CapitalState = db.Column(db.String(100))
    NationalBird = db.Column(db.String(100))
    CountryPopulation = db.Column(db.BigInteger)


# Define the route to insert country information
@app.route('/api/country', methods=['POST'])
def insert_country_info():
    try:
        # Parse the JSON data from the request
        country_data = request.get_json()

        # Log the data received in the request
        app.logger.debug("Received data: %s", country_data)

        # Create a CountryInfo object from the JSON data
        country_info = CountryInfo(
            CountryName=country_data['country_name'],
            CapitalState=country_data['capital_state'],
            NationalBird=country_data['national_bird'],
            CountryPopulation=country_data['country_population']
        )

        # Add the country_info object to the database
        db.session.add(country_info)
        db.session.commit()

        # Return the inserted CountryId as a response
        return jsonify({'CountryId': country_info.CountryId}), 201

    except Exception as e:
        app.logger.exception("An error occurred while processing the request:")
        return jsonify({'error': 'An error occurred while processing the request.'}), 500


if __name__ == "__main__":
    # Run the Flask app on the specified host and port
    app.run(host='0.0.0.0', port=5000, debug=True)
