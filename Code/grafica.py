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
    cursor.execute("SELECT tiempo,temperatura, pH, conductividad_electrica, oxigeno_disuelto FROM lecturas")
    # Fetch all the rows
    rows = cursor.fetchall()
    #list comprehension to retrieve values
    tiempo = [row[0].strftime("%H:%M:%S") for row in rows]
    temp = [float(row[1]) for row in rows]
    pH = [float(row[2]) for row in rows]
    EC = [float(row[3]) for row in rows]
    ox = [float(row[4]) for row in rows]
    return tiempo,temp, pH, EC, ox

def printVariables():
    print("Tiempo",tiempo)
    print("Temp = ", temp)
    for temperature in temp:
        print(temperature)
    print("pH= ", pH)
    print("EC= ", EC)
    print("Ox= ", ox)

def plotVariables():
    plt.figure(figsize=(12,8))
    plt.subplot(2,2,1)
    plt.scatter(tiempo, temp)
    plt.xlabel("Tiempo")
    plt.ylabel("Temperatura")
    plt.title("temp graph")
    
    plt.subplot(2,2,2)
    plt.scatter(tiempo, pH)
    plt.xlabel("Tiempo")
    plt.ylabel("pH")
    plt.title("pH graph")

    plt.subplot(2,2,3)
    plt.scatter(tiempo, EC)
    plt.xlabel("Tiempo")
    plt.ylabel("EC")
    plt.title("EC graph")

    plt.subplot(2,2,4)
    plt.scatter(tiempo, ox)
    plt.xlabel("Tiempo")
    plt.ylabel("ox")
    plt.title("ox graph")

    plt.show()

tiempo,temp, pH, EC, ox = getVariables()

printVariables()

plotVariables()
