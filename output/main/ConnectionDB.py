import mysql.connector
import os
import pymysql

# Database configuration
DB_details = ["","","",""]
#DB_details_file = "mysql_config.txt"
DB_details_file = os.path.join(os.path.dirname(__file__), "mysql_config.txt")

with open (DB_details_file,'r') as file:
    for line in file:
        # Find the start and end indices of the text within double quotation marks
        start_index = line.find('"')
        end_index = line.find('"', start_index + 1)

        # Extract the text and append to the list
        if start_index != -1 and end_index != -1:
            extracted_text = line[start_index + 1: end_index]
            if line.startswith("host"):
                DB_details[0] = extracted_text
            if line.startswith("user"):
                DB_details[1] = extracted_text
            if line.startswith("password"):
                DB_details[2] = extracted_text
            if line.startswith("database"):
                DB_details[3] = extracted_text


host = DB_details[0]
user = DB_details[1]
password = DB_details[2]
database = DB_details[3]


# Create a connection
try:
    #connection = mysql.connector.connect(
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
    )

    if connection.open():
        print("Connected to MySQL database")

    # Perform database operations here

except Exception as e:
    print("Error connecting to MySQL database:", e)

def get_connection():
    # Return the connection object
    return connection

def close_connection():
    #Close the connection when done
   if 'connection' in locals() and connection.is_connected():
       connection.close()
       print("Connection closed")
