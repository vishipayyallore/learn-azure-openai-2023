from flask import Blueprint, request, jsonify
from utils.GetCountryInfoFromAzureOpenAI import GetCountryInfoFromAzureOpenAI
from models.models import CountryInfoDto

api_routes_bp = Blueprint('api_routes', __name__)

# Create an instance of the GetCountryInfoFromAzureOpenAI class
openai_helper = GetCountryInfoFromAzureOpenAI()

# Define the route to insert country information


@api_routes_bp.route('/api/countryinfov1', methods=['POST'])
def insert_country_info_v1():
    try:
        # Parse the JSON data from the request
        country_data = request.get_json()

        # Get the country information from Azure OpenAI
        country_name = country_data.get('country_name')
        country_data = openai_helper.get_country_info(country_name)

        # Create a CountryInfoDto object from the JSON data
        country_info = CountryInfoDto(
            CountryName=country_data['country_name'],
            CapitalState=country_data['capital_state'],
            NationalBird=country_data['national_bird'],
            CountryPopulation=country_data['country_population']
        )

        # Save the country_info object to the database
        country_info.save()

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
        return jsonify({'error': 'An error occurred while processing the request.'}), 500
