import mysql.connector

# Database configuration
DB_details = ["","","",""]
DB_details_file = "mysql_config.txt"

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
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    if connection.is_connected():
        print("Connected to MySQL database")

    # Perform database operations here

except mysql.connector.Error as e:
    print("Error connecting to MySQL database:", e)

def close_connection():
    #Close the connection when done
   if 'connection' in locals() and connection.is_connected():
       connection.close()
       print("Connection closed")
