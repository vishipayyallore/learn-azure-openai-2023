import json
import pyodbc

from CountryInfo import CountryInfo

from dotenv import dotenv_values
config_details = dotenv_values(".env")


def insert_country_info(connection_string, country_info):

    try:
        conn = pyodbc.connect(connection_string)
        print("Connection to the SQL Server database is successful.")

        # Create a cursor
        cursor = conn.cursor()

        # Prepare the SQL statement to execute the stored procedure
        sql = "{CALL usp_insert_country_info (?, ?, ?, ?, ?)}"

        # Prepare the parameters for the stored procedure
        params = (country_info.country_name, country_info.capital_state,
                  country_info.national_bird, country_info.country_population, country_info.country_id)

        # Execute the stored procedure to insert data into the table
        cursor.execute(sql, params)
        
        # Fetch the output parameter value (CountryId)
        # country_info.country_id = params[4]
        country_info.country_id = cursor.fetchval()

        # Commit the transaction
        conn.commit()

        print("Country information inserted with CountryId:",
              country_info.country_id)

    except pyodbc.Error as e:
        print("Error connecting to the SQL Server database:", e)
    finally:
        if conn:
            # Close the cursor and connection
            cursor.close()
            conn.close()
            print("Connection closed.")


# Example usage:
if __name__ == "__main__":
    connection_string = config_details['SQLSERVERCONNECTIONSTRING']

    # Sample JSON object representing country info
    json_data = '''
    {
        "country_name": "Sample Country",
        "capital_state": "Sample Capital",
        "national_bird": "Sample Bird",
        "country_population": 1000000,
        "country_id": 0
    }
    '''

    # Parse the JSON object and create a CountryInfo object
    country_info_dict = json.loads(json_data)
    country_info = CountryInfo(**country_info_dict)

    # Insert the country information into the database
    insert_country_info(connection_string, country_info)
