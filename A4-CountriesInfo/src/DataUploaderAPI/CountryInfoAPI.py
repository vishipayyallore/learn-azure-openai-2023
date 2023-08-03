import logging
from flask import Flask, request, jsonify
import pyodbc
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values
from urllib.parse import quote_plus  # Import the quote_plus function
from GetCountryInfoFromAzureOpenAI import GetCountryInfoFromAzureOpenAI

app = Flask(__name__)

# Load configuration from .env file
config_details = dotenv_values(".env")

connection_string = config_details["SQLSERVERCONNECTIONSTRING"]
# Print the connection string
print(connection_string)

# Configure the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_details['SQLALCHEMY_TRACK_MODIFICATIONS']
db = SQLAlchemy(app)

# Create an instance of the GetCountryInfoFromAzureOpenAI class
openai_helper = GetCountryInfoFromAzureOpenAI()

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
@app.route('/api/countryinfo', methods=['POST'])
def insert_country_info():
    try:
        # Parse the JSON data from the request
        country_data = request.get_json()

        # Log the data received in the request
        app.logger.debug("Received data: %s", country_data)

        # Get the country information from Azure OpenAI
        country_name = country_data.get('country_name')
        country_data = openai_helper.get_country_info(country_name)

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

        # Return the inserted CountryInfo as a response
        response_data = {
            'CountryId': country_info.CountryId,
            'CountryName': country_info.CountryName,
            'CapitalState': country_info.CapitalState,
            'NationalBird': country_info.NationalBird,
            'CountryPopulation': country_info.CountryPopulation
        }

        return jsonify(response_data), 201

    except Exception as e:
        app.logger.exception("An error occurred while processing the request:")
        return jsonify({'error': 'An error occurred while processing the request.'}), 500


if __name__ == "__main__":
    # Run the Flask app on the specified host and port
    app.run(host='0.0.0.0', port=5000, debug=True)
