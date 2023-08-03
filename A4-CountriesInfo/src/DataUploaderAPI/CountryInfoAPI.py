from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import dotenv_values
import pyodbc

app = Flask(__name__)

# Load configuration from .env file
config_details = dotenv_values(".env")

# Configure the SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = config_details['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config_details['SQLALCHEMY_TRACK_MODIFICATIONS']
db = SQLAlchemy(app)


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
        return jsonify({'error': 'An error occurred while processing the request.'}), 500


if __name__ == "__main__":
    # Run the Flask app on the specified host and port
    app.run(host='0.0.0.0', port=5000, debug=True)
