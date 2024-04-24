import serial
import sys
import time
import os
import re
import RPi.GPIO as GPIO
import mysql.connector
from datetime import datetime
import grafica
import WQIFormula as WQI
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage 
#Path para la gui es establecido
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/pi/Tesis/Thesis/Code/GUI/build/assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
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
    temp = 0
    conductividad = 0
    potencialHidrogeno = 0
    indice=0
    calidad=None

    mediciones = {
    'tiempo': datetime.now(),
    'temperatura': 0,
    'conductividad_electrica': 0,
    'pH': 0,
    'oxigeno_disuelto': 0, 
    'indice': 0,
    'calidad': None
    }

    #medición de temperatura
    one_wire_temps = getTemperatures()

    if one_wire_temps:
        temp = one_wire_temps[0]
        mediciones['temperatura'] = temp
    else:
        print("Error al leer la temperatura")

    #medición de conductividad
    send_cmd(sensor1, "R")
    lines1 = read_lines(sensor1)
    for line in lines1:
        if line.startswith(b'OK'):
            continue
        elif line.startswith(b'*ER'):
            print("Comando desconocido en el sensor 1")
            continue
        elif line.startswith(b'*OV'):
            print("Sobrevoltaje en el sensor 1 (VCC>=5.5V)")
            continue
        elif line.startswith(b'*UV'):
            conductividad = conductividad  # Usar valor anterior
            print("Bajo voltaje")
            continue
        elif line.startswith(b'*RS'):
            print("Sensor 1 reseteado")
            continue
        elif line.startswith(b'*RE'):
            print("Sensor 1 iniciado")
            continue
        elif line.startswith(b'*SL'):
            print("Sensor 1 entrando en modo de suspensión")
            continue
        elif line.startswith(b'*WA'):
            print("Sensor 1 saliendo del modo de suspensión")
            continue
        else:
            try:
                conductividad = float(line.decode('utf-8'))
                mediciones['conductividad_electrica'] = conductividad
            except ValueError:
                print("valueerror")
                continue
    #medición de pH
    send_cmd(sensor2, "R")
    lines2 = read_lines(sensor2)
    for line in lines2:
        if line.startswith(b'OK'):
            continue
        elif line.startswith(b'*ER'):
            print("Comando desconocido en el sensor 2")
            continue
        elif line.startswith(b'*OV'):
            print("Sobrevoltaje en el sensor 2 (VCC>=5.5V)")
            continue
        elif line.startswith(b'*UV'):
            potencialHidrogeno = potencialHidrogeno  # Usar valor anterior
            print("Bajo voltaje")
            continue
        elif line.startswith(b'*RS'):
            print("Sensor 2 reseteado")
            continue
        elif line.startswith(b'*RE'):
            print("Sensor 2 iniciado")
            continue
        elif line.startswith(b'*SL'):
            print("Sensor 2 entrando en modo de suspensión")
            continue
        elif line.startswith(b'*WA'):
            print("Sensor 2 saliendo del modo de suspensión")
            continue
        else:
            try:
                potencialHidrogeno = float(line.decode('utf-8'))
                mediciones['pH'] = potencialHidrogeno
            except ValueError:
                continue

    #Cálculo del índice
    #valor de OD de prueba
    oxigenoDisuelto=6
    P=WQI.parametrizacion(conductividad,temp,potencialHidrogeno,oxigenoDisuelto)
    indice =WQI.calculo(P,[1,2,3,4])
    mediciones['indice'] = indice
    calidad=WQI.interpretacion(indice)
    mediciones['calidad'] = calidad
    return mediciones


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
    # Se abren los puertos serial
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

    # Create the GUI
    window = Tk()
    window.title("Sistema de Adquisición de Datos")
    window.geometry("1280x720")
    window.configure(bg="#FFFFFF")

    # Se crea el fondo
    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=720,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)

    # Se añaden  las imágenes de las lecturas
    image_image_1 = PhotoImage(
        file=relative_to_assets("image_1.png"))
    image_1 = canvas.create_image(
        627.0,
        122.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets("image_2.png"))
    image_2 = canvas.create_image(
        627.0,
        264.0,
        image=image_image_2
    )

    image_image_3 = PhotoImage(
        file=relative_to_assets("image_3.png"))
    image_3 = canvas.create_image(
        627.0,
        406.0,
        image=image_image_3
    )

    image_image_4 = PhotoImage(
        file=relative_to_assets("image_4.png"))
    image_4 = canvas.create_image(
        627.0,
        548.0,
        image=image_image_4
    )

    image_image_5 = PhotoImage(
        file=relative_to_assets("image_5.png"))
    image_5 = canvas.create_image(
        627.0,
        673.0,
        image=image_image_5
    )

    # Se añaden los textos de las lecturas
    pHText = canvas.create_text(
        318.0,
        104.0,
        anchor="nw",
        text="pH: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )

    conductividadText = canvas.create_text(
        318.0,
        246.0,
        anchor="nw",
        text="Conductividad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )

    temperaturaText = canvas.create_text(
        318.0,
        388.0,
        anchor="nw",
        text="Temperatura: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )

    indiceText = canvas.create_text(
        318.0,
        530.0,
        anchor="nw",
        text="Índice de Calidad de Agua: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )

    calidadText = canvas.create_text(
        318.0,
        655.0,
        anchor="nw",
        text="Calidad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )

    # Se definen las funciones
    def actualizarDatos():

        mediciones = poll_sensors(sensor1, sensor2, usbports[0], usbports[1])
        print("Tiempo:", mediciones['tiempo'])
        print("Temperatura:", mediciones['temperatura'])
        print("Conductividad eléctrica:", mediciones['conductividad_electrica'])
        print("pH:", mediciones['pH'])
        print("Oxígeno disuelto:", mediciones['oxigeno_disuelto'])
        print("Índice:", mediciones['indice'])
        print("Calidad:", mediciones['calidad'])

        pHValor = mediciones['pH']
        canvas.itemconfig(tagOrId=pHText, text=f"ph: {pHValor}")

        conductividadValor = mediciones['conductividad_electrica']
        canvas.itemconfig(tagOrId=conductividadText, text=f"Conductividad: {conductividadValor}")

        temperaturaValor = mediciones['temperatura']
        canvas.itemconfig(tagOrId=temperaturaText, text=f"Temperatura: {temperaturaValor}")

        indice = mediciones['indice']
        canvas.itemconfig(tagOrId=indiceText, text=f"Índice de Calidad de Agua: {indice}")

        calidad = mediciones['calidad']
        canvas.itemconfig(tagOrId=calidadText, text=calidad)
    
    def detenerMediciones(): 
        raise KeyboardInterrupt
        
    def medirContinuamente():
        try:
            while True:
                print("I'm running")
                time.sleep(1)  # Sample time
        except KeyboardInterrupt:
            print("Loop stopped")


    # Se crean los botones
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=medirContinuamente,
        relief="flat"
    )
    button_1.place(
        x=31.0,
        y=482.0,
        width=143.0,
        height=92.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=detenerMediciones,
        relief="flat"
    )
    button_2.place(
        x=31.0,
        y=596.0,
        width=143.0,
        height=92.0
    )

    # Se insertan los logos
    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6.png"))
    image_6 = canvas.create_image(
        68.0,
        90.0,
        image=image_image_6
    )

    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7.png"))
    image_7 = canvas.create_image(
        1195.0,
        76.0,
        image=image_image_7
    )

    # Se crea el header
    canvas.create_text(
        385.0,
        10.0,
        anchor="nw",
        text="Sistema de Adquisición de Datos",
        fill="#000000",
        font=("NunitoSans Regular", 32 * -1)
    )

    window.resizable(False, False)
    window.mainloop()
    