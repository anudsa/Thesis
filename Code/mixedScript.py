import serial
import sys
import time
import os
import re
import RPi.GPIO as GPIO
import mysql.connector
from datetime import datetime
#Database connection
mysql_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Pa$$w0rd",
    database="Sensores"
)
# Create a cursor object to execute SQL queries
cursor = mysql_db.cursor()
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
    print("Leyendo sensores del puerto usb {} y {}: ".format(usbport1, usbport2))
    temp = 0
    conductividad = 0
    potencialHidrogeno = 0
    while True:
        one_wire_temps = getTemperatures()

        if one_wire_temps:
            temp = one_wire_temps[0]
            print("Temperatura: {:.2f}°C".format(temp))
        else:
            print("Error al leer la temperatura")

        send_cmd(sensor1, "R")
        lines1 = read_lines(sensor1)
        for i in range(len(lines1)):
            if lines1[i][0] != b'*'[0]:
                conductividad = float(lines1[i].decode('utf-8'))  #Cast a float
                print("Conductividad Eléctrica: {}".format(conductividad))

        send_cmd(sensor2, "R")
        lines2 = read_lines(sensor2)
        for i in range(len(lines2)):
            if lines2[i][0] != b'*'[0]:
                potencialHidrogeno = float(lines2[i].decode('utf-8'))  #Cast a float
                print("pH: {}".format(potencialHidrogeno))

        # Después de tomar todas las mediciones, se guardan en un diccionario:
        mediciones = {
            'tiempo': datetime.now(),
            'temperatura': temp,
            'conductividad_electrica': conductividad,
            'pH': potencialHidrogeno,
            'oxigeno_disuelto': 6  # Assuming you have a default value
        }
        # Se añaden a la base de datos
        addData(mediciones)
        time.sleep(1)  # Tiempo de muestreo

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


#Main script
if __name__ == "__main__":
    usbports = ['/dev/ttyUSB0', '/dev/ttyUSB1']
    
    #Se abren los puertos serial
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

    try:
        poll_sensors(sensor1, sensor2, usbports[0], usbports[1])
    except KeyboardInterrupt: 		# catches the ctrl-c command, which breaks the loop above
        print("Se han detenido las mediciones.")
        print("Información almacenada:")
        printAllLectures()
        closeConnection()