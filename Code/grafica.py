import numpy as np 
import matplotlib.pyplot as plt  
import mysql.connector
import decimal  # Import the decimal module
mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pa$$w0rd",
    database="Sensores"
)
# Create a cursor object to execute SQL queries
cursor = mysql_db.cursor()

def getVariables(id_inicial,id_final):
    # Execute the SELECT query
    cursor.execute(f"SELECT tiempo, temperatura, pH, conductividad, indice FROM lecturas WHERE id BETWEEN {id_inicial} AND {id_final}")
    # Fetch all the rows
    rows = cursor.fetchall()
    #list comprehension to retrieve values
    tiempo = [row[0].strftime("%H:%M:%S") for row in rows]
    temperatura = [float(row[1]) for row in rows]
    pH = [float(row[2]) for row in rows]
    conductividad = [float(row[3]) for row in rows]
    indice = [float(row[4]) for row in rows]
    return tiempo,temperatura, pH, conductividad, indice

def printVariables(tiempo,temperatura,pH,conductividad,indice):
    print("Tiempo",tiempo)
    print("temperatura = ", temperatura)
    for temperature in temperatura:
        print(temperature)
    print("pH= ", pH)
    print("conductividad= ", conductividad)
    print("indice= ", indice)

def plotVariables(tiempo,temperatura, pH, conductividad, indice):
    plt.figure(figsize=(12,8))
    plt.subplot(2,2,1)
    plt.subplots_adjust(hspace=0.5)
    plt.scatter(tiempo, temperatura)
    plt.xlabel("Tiempo")
    plt.ylabel("Temperatura")
    plt.title("temperatura ")
    plt.xticks(rotation='vertical')

    plt.subplot(2,2,2)
    plt.scatter(tiempo, pH)
    plt.xlabel("Tiempo")
    plt.ylabel("pH")
    plt.title("pH ")
    plt.xticks(rotation='vertical')

    plt.subplot(2,2,3)
    plt.scatter(tiempo, conductividad)
    plt.xlabel("Tiempo")
    plt.ylabel("conductividad")
    plt.title("conductividad ")
    plt.xticks(rotation='vertical')

    plt.subplot(2,2,4)
    plt.scatter(tiempo, indice)
    plt.xlabel("Tiempo")
    plt.ylabel("indice")
    plt.title("indice ")
    plt.xticks(rotation='vertical')

    plt.show()
    #plt.pause(10)


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

def graficarParametros(id_inicial,id_final):
    tiempo,temperatura, pH, conductividad, indice = getVariables(id_inicial,id_final)
    printVariables(tiempo,temperatura, pH, conductividad, indice)
    plotVariables(tiempo,temperatura, pH, conductividad, indice)


if __name__ == "__main__":
    graficarParametros(7,11)
    printAllLectures()