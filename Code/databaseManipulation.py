#Script to test the python-databse connection
import mysql.connector
from datetime import datetime

mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pa$$w0rd",
    database="Sensores"
)

# Create a cursor object to execute SQL queries
cursor = mysql_db.cursor()

#Sample data for testing purposes
sampleData = {
    'tiempo': datetime.now(),
    'temperatura': 20.5,
    'pH': 4.8,
    'conductividad_electrica': 330.0,
    'oxigeno_disuelto': 2
}

#Function to print databases list
def printDatabases():
    cursor.execute("show databases")
    # Fetch all the rows
    databases = cursor.fetchall()
    # Print the list of databases
    for database in databases:
        print(database[0])

#Function to print all date from the table lecturas
def printAllLectures():
    # Execute the SELECT query
    cursor.execute("SELECT * FROM lecturas")
    # Fetch all the rows
    rows = cursor.fetchall()
    # Print the column names
    columns = [description[0] for description in cursor.description]
    print(columns)
    #Print the data
    for row in rows:
        values = [str(value) if not isinstance(value, (int, float)) else value for value in row]
        print(values)

#Function to add data
def addData(Data):
    # Create the INSERT query
    insert_query = "INSERT INTO lecturas (tiempo, temperatura, pH, conductividad_electrica, oxigeno_disuelto) VALUES (%s, %s, %s, %s, %s)"
    # Execute the INSERT query with the values
    cursor.execute(insert_query, (Data['tiempo'], Data['temperatura'], Data['pH'], Data['conductividad_electrica'], Data['oxigeno_disuelto']))
    # Commit the changes to the database
    mysql_db.commit()

def removeLastRow():
    # Create the DELETE query with ORDER BY and LIMIT
    delete_query = "DELETE FROM lecturas ORDER BY id DESC LIMIT 1"
    # Execute the DELETE query
    cursor.execute(delete_query)
    # Commit the changes to the database
    mysql_db.commit()

def removeRowById(row_id):
    # Create the DELETE query with WHERE clause
    delete_query = "DELETE FROM lecturas WHERE id = %s"
    # Execute the DELETE query with the specified row_id
    cursor.execute(delete_query, (row_id,))
    # Commit the changes to the database
    mysql_db.commit()

def closeConnection():
    # Close the cursor and connection
    cursor.close()
    mysql_db.close()

print("Printing all databases with python:")
printDatabases()
print("Printing all data from table with python:")
printAllLectures()

choice= input("type 1 to add data, 2 to remove last row, 3 to remove row by id: ")
if choice == "1" : 
    print("adding data: ")
    addData(sampleData)
    printAllLectures()
elif choice == "2":
    print("removing data: ")
    removeLastRow()
    printAllLectures()
elif choice=="3":
    row_id=input("Enter the row id:")
    removeRowById(row_id)
    printAllLectures()
    print(f"Row with ID {row_id} removed")