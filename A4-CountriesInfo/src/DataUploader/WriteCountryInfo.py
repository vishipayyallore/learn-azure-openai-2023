import pyodbc

from dotenv import dotenv_values
config_details = dotenv_values(".env")

def insert_country_info(connection_string, country_name, capital_state, national_bird, country_population):
    try:
        # Connect to the SQL Server database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Prepare the SQL statement to execute the stored procedure
        sql = "{CALL usp_insert_country_info (?, ?, ?, ?, ?)}"

        # Prepare the parameters for the stored procedure
        params = (country_name, capital_state, national_bird, country_population, None)

        # Execute the stored procedure to insert data into the table
        cursor.execute(sql, params)
        conn.commit()

        # Retrieve the output parameter value (CountryId)
        country_id = params[4]
        print(f"Data inserted successfully. CountryId: {country_id}")
    except pyodbc.Error as ex:
        print("Error:", ex)
    finally:
        if conn:
            conn.close()

# Example usage:
if __name__ == "__main__":
    connection_string = config_details['SQLSERVERCONNECTIONSTRING']

    country_name = "Sample Country"
    capital_state = "Sample Capital"
    national_bird = "Sample Bird"
    country_population = 1000000

    insert_country_info(connection_string, country_name, capital_state, national_bird, country_population)
