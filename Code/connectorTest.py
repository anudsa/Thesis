#Script to test the python-databse connection
import mysql.connector
from datetime import datetime

mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pa$$w0rd",
    database="Sensores"
)
print(mysql_db)
# Create a cursor object to execute SQL queries
cursor = mysql_db.cursor()
cursor.execute("show databases")

# Fetch all the rows
databases = cursor.fetchall()
# Print the list of databases
for database in databases:
    print(database[0])

#select query

# Execute the SELECT query
cursor.execute("SELECT * FROM lecturas")

# Fetch all the rows
rows = cursor.fetchall()

# Print the column names
columns = [description[0] for description in cursor.description]
print(columns)

# Print the data
for row in rows:
    values = [str(value) if not isinstance(value, (int, float)) else value for value in row]
    print(values)


#adding data

# Example data for the new row
new_row_sample_data = {
    'tiempo': datetime.now(),
    'temperatura': 27.5,
    'pH': 6.8,
    'conductividad_electrica': 600.0,
    'oxigeno_disuelto': 7.8
}
# Create the INSERT query
insert_query = "INSERT INTO lecturas (tiempo, temperatura, pH, conductividad_electrica, oxigeno_disuelto) VALUES (%s, %s, %s, %s, %s)"

# Execute the INSERT query with the values
cursor.execute(insert_query, (new_row_sample_data['tiempo'], new_row_sample_data['temperatura'], new_row_sample_data['pH'], new_row_sample_data['conductividad_electrica'], new_row_sample_data['oxigeno_disuelto']))

# Commit the changes to the database
mysql_db.commit()

# Close the cursor and connection
cursor.close()
mysql_db.close()
