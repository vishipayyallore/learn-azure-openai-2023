import pyodbc

# Function to call the stored procedure and insert data into the database
def insert_data_with_stored_proc(connection_string, country_id, country_name, capital_state, country_bird, country_population):
    try:
        # Establish a connection to the database
        with pyodbc.connect(connection_string) as conn:
            # Create a cursor to execute SQL queries
            cursor = conn.cursor()

            # Call the stored procedure with parameters
            cursor.execute("{CALL usp_insert_country_info(?, ?, ?, ?, ?)}",
                           (country_id, country_name, capital_state, country_bird, country_population))

            # Commit the changes to the database
            conn.commit()

            print("Data inserted successfully.")
    except pyodbc.Error as e:
        print(f"Error inserting data: {e}")

# Sample data
country_id = 1
country_name = "United States"
capital_state = "Washington, D.C."
country_bird = "Bald Eagle"
country_population = 328200000

# Connection string for your Azure SQL Server database
connection_string = "Driver={SQL Server};Server=myserver.database.windows.net;Database=mydb;UID=myuser;PWD=mypassword"

# Call the function to insert data using the stored procedure
insert_data_with_stored_proc(connection_string, country_id, country_name, capital_state, country_bird, country_population)
