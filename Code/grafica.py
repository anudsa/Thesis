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

def getVariables():
    # Execute the SELECT query
    cursor.execute("SELECT tiempo, temperatura, pH, conductividad, indice FROM lecturas")
    # Fetch all the rows
    rows = cursor.fetchall()
    #list comprehension to retrieve values
    tiempo = [row[0].strftime("%H:%M:%S") for row in rows]
    temperatura = [float(row[1]) for row in rows]
    pH = [float(row[2]) for row in rows]
    conductividad = [float(row[3]) for row in rows]
    indice = [float(row[4]) for row in rows]
    return tiempo,temperatura, pH, conductividad, indice

def printVariables():
    print("Tiempo",tiempo)
    print("temperatura = ", temperatura)
    for temperature in temperatura:
        print(temperature)
    print("pH= ", pH)
    print("conductividad= ", conductividad)
    print("indice= ", indice)

def plotVariables():
    plt.figure(figsize=(12,8))
    plt.subplot(2,2,1)
    plt.scatter(tiempo, temperatura)
    plt.xlabel("Tiempo")
    plt.ylabel("Temperatura")
    plt.title("temperatura graph")
    
    plt.subplot(2,2,2)
    plt.scatter(tiempo, pH)
    plt.xlabel("Tiempo")
    plt.ylabel("pH")
    plt.title("pH graph")

    plt.subplot(2,2,3)
    plt.scatter(tiempo, conductividad)
    plt.xlabel("Tiempo")
    plt.ylabel("conductividad")
    plt.title("conductividad graph")

    plt.subplot(2,2,4)
    plt.scatter(tiempo, indice)
    plt.xlabel("Tiempo")
    plt.ylabel("indice")
    plt.title("indice graph")

    plt.show()
    plt.pause(10)

tiempo,temperatura, pH, conductividad, indice = getVariables()

if __name__ == "__main__":
    printVariables()
    plotVariables()