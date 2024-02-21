import serial
import sys
import time
import os
import re
import RPi.GPIO as GPIO

#function to get temperatures
def getTemperatures():
    allTemps = list()
    onewire_basedir = "/sys/bus/w1/devices/"
    onewire_devices = os.listdir(onewire_basedir)
    onewire_retemp = re.compile('t=(\d*)')

    for device_string in onewire_devices:
        if device_string.startswith("28"):
            onewire_path = os.path.join(onewire_basedir, device_string, "w1_slave")
            onewire_devfile = open(onewire_path, "r")
            onewire_devtext = onewire_devfile.readlines()
            onewire_temp = onewire_retemp.search(onewire_devtext[1])
            temperature = int(onewire_temp.group(1)) / 1000.0
            allTemps.append(temperature)

    return allTemps

def read_line(sensor):
    lsl = len(b'\r')
    line_buffer = []
    while True:
        next_char = sensor.read(1)
        if next_char == b'':
            break
        line_buffer.append(next_char)
        if len(line_buffer) >= lsl and line_buffer[-lsl:] == [b'\r']:
            break
    return b''.join(line_buffer)

def read_lines(sensor):
    lines = []
    try:
        while True:
            line = read_line(sensor)
            if not line:
                break
            sensor.flushInput()
            lines.append(line)
        return lines
    except serial.SerialException as e:
        print("Error: ", e)
        return None

def send_cmd(sensor, cmd):
    buf = cmd + "\r"
    try:
        sensor.write(buf.encode('utf-8'))
        return True
    except serial.SerialException as e:
        print("Error: ", e)
        return None

def poll_sensors(sensor1, sensor2, usbport1, usbport2):
    print("Polling sensors connected to {} and {}: ".format(usbport1, usbport2))

    while True:
        one_wire_temps = getTemperatures()

        if one_wire_temps:
            print("Temperature from One-Wire Sensor: {:.2f}°C".format(one_wire_temps[0]))
        else:
            print("Unable to read temperature from One-Wire Sensor.")

        send_cmd(sensor1, "R")
        lines1 = read_lines(sensor1)
        for i in range(len(lines1)):
            if lines1[i][0] != b'*'[0]:
                print("Response from {}: {}".format(usbport1, lines1[i].decode('utf-8')))

        send_cmd(sensor2, "R")
        lines2 = read_lines(sensor2)
        for i in range(len(lines2)):
            if lines2[i][0] != b'*'[0]:
                print("Response from {}: {}".format(usbport2, lines2[i].decode('utf-8')))

        time.sleep(1)  # Adjust as needed

if __name__ == "__main__":
    usbports = ['/dev/ttyUSB0', '/dev/ttyUSB1']

    try:
        sensor1 = serial.Serial(usbports[0], 9600, timeout=0)
    except serial.SerialException as e:
        print("Error opening serial port {}: {}".format(usbports[0], e))
        sys.exit(1)

    try:
        sensor2 = serial.Serial(usbports[1], 9600, timeout=0)
    except serial.SerialException as e:
        print("Error opening serial port {}: {}".format(usbports[1], e))
        sys.exit(1)

    poll_sensors(sensor1, sensor2, usbports[0], usbports[1])

#############################
    
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
    'conductividad_eléctrica': 330.0,
    'oxígeno_disuelto': 2
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
    insert_query = "INSERT INTO lecturas (tiempo, temperatura, pH, conductividad_eléctrica, oxígeno_disuelto) VALUES (%s, %s, %s, %s, %s)"
    # Execute the INSERT query with the values
    cursor.execute(insert_query, (Data['tiempo'], Data['temperatura'], Data['pH'], Data['conductividad_eléctrica'], Data['oxígeno_disuelto']))
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