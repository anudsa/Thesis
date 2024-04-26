from pathlib import Path
from tkinter import *
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
import threading	

#Path para la gui es establecido
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/pi/Tesis/Thesis/Code/GUI/Homescreen/build/assets/frame0")
	
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

#### Main Script ###
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
    
    # Se crea la GUI

    def show_frame(frame):
        frame.tkraise()

	
    window = Tk()
    window.title("Sistema de Adquisición de Datos")
    window.geometry("1280x720")
    
    
    medicionContinua = Frame(window)
    medicionEnIntervalos = Frame(window)
    medicionPuntual = Frame(window)
    
    # Initially hide frames other than Homescreen
    medicionPuntual.grid(row=0, column=0)
    medicionContinua.grid(row=0, column=0)
    medicionEnIntervalos.grid(row=0, column=0)
    

    ##### Medicion En Intervalos ####
    #Fondo
    canvas_intervalos = Canvas(
        medicionEnIntervalos,
        bg = "#FFFFFF",
        height = 720,
        width = 1280,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas_intervalos.pack()
    #Imagenes
    image_image_1_intervalos = PhotoImage(
        file=relative_to_assets("image_1_intervalos.png"))
    image_1_intervalos = canvas_intervalos.create_image(
        641.0,
        141.0,
        image=image_image_1_intervalos
    )
    
    image_image_2_intervalos = PhotoImage(
        file=relative_to_assets("image_2_intervalos.png"))
    image_2_intervalos = canvas_intervalos.create_image(
        641.0,
        253.0,
        image=image_image_2_intervalos
    )
    
    image_image_3_intervalos = PhotoImage(
        file=relative_to_assets("image_3_intervalos.png"))
    image_3_intervalos = canvas_intervalos.create_image(
        637.0,
        365.0,
        image=image_image_3_intervalos
    )
    
    image_image_4_intervalos = PhotoImage(
        file=relative_to_assets("image_4_intervalos.png"))
    image_4_intervalos = canvas_intervalos.create_image(
        637.0,
        477.0,
        image=image_image_4_intervalos
    )
    
    image_image_5_intervalos = PhotoImage(
        file=relative_to_assets("image_5_intervalos.png"))
    image_5_intervalos = canvas_intervalos.create_image(
        637.0,
        589.0,
        image=image_image_5_intervalos
    )
    
    image_image_6_intervalos = PhotoImage(
        file=relative_to_assets("image_6_intervalos.png"))
    image_6_intervalos = canvas_intervalos.create_image(
        57.0,
        87.0,
        image=image_image_6_intervalos
    )
    
    image_image_7_intervalos = PhotoImage(
        file=relative_to_assets("image_7_intervalos.png"))
    image_7_intervalos = canvas_intervalos.create_image(
        1205.0,
        67.0,
        image=image_image_7_intervalos
    )
    
    image_image_8_intervalos = PhotoImage(
        file=relative_to_assets("image_8_intervalos.png"))
    image_8_intervalos = canvas_intervalos.create_image(
        456.0,
        684.0,
        image=image_image_8_intervalos
    )
    
    image_image_9_intervalos = PhotoImage(
        file=relative_to_assets("image_9_intervalos.png"))
    image_9_intervalos = canvas_intervalos.create_image(
        785.0,
        684.0,
        image=image_image_9_intervalos
    )
    #Texto
    pHText_intervalos=canvas_intervalos.create_text(
        332.0,
        123.0,
        anchor="nw",
        text="pH: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    conductividadText_intervalos=canvas_intervalos.create_text(
        332.0,
        235.0,
        anchor="nw",
        text="Conductividad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    temperaturaText_intervalos=canvas_intervalos.create_text(
        328.0,
        347.0,
        anchor="nw",
        text="Temperatura: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    indiceText_intervalos=canvas_intervalos.create_text(
        328.0,
        459.0,
        anchor="nw",
        text="Índice de Calidad de Agua: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    calidadText_intervalos=canvas_intervalos.create_text(
        328.0,
        571.0,
        anchor="nw",
        text="Calidad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    #Botones
    button_image_1_intervalos = PhotoImage(
        file=relative_to_assets("button_1_intervalos.png"))
    button_1_intervalos = Button(medicionEnIntervalos,
        image=button_image_1_intervalos,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_1_intervalos clicked"),
        relief="flat"
    )
    button_1_intervalos.place(
        x=116.0,
        y=297.0,
        width=143.0,
        height=92.0
    )
    
    button_image_2_intervalos = PhotoImage(
        file=relative_to_assets("button_2_intervalos.png"))
    button_2_intervalos = Button(medicionEnIntervalos,
        image=button_image_2_intervalos,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_2_intervalos clicked"),
        relief="flat"
    )
    button_2_intervalos.place(
        x=1027.0,
        y=297.0,
        width=143.0,
        height=92.0
    )
    
    button_image_3_intervalos = PhotoImage(
        file=relative_to_assets("button_3_intervalos.png"))
    button_3_intervalos = Button(medicionEnIntervalos,
        image=button_image_3_intervalos,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3_intervalos clicked"),
        relief="flat"
    )
    button_3_intervalos.place(
        x=1027.0,
        y=401.0,
        width=143.0,
        height=92.0
    )
    
    button_image_4_intervalos = PhotoImage(
        file=relative_to_assets("button_4_intervalos.png"))
    button_4_intervalos = Button(medicionEnIntervalos,
        image=button_image_4_intervalos,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4_intervalos clicked"),
        relief="flat"
    )
    button_4_intervalos.place(
        x=943.0,
        y=655.0,
        width=60.0,
        height=59.0
    )
    
    button_image_5_intervalos = PhotoImage(
        file=relative_to_assets("button_5_intervalos.png"))
    button_5_intervalos = Button(medicionEnIntervalos,
        image=button_image_5_intervalos,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_frame(Homescreen),  #Home
        relief="flat"
    )
    button_5_intervalos.place(
        x=1180.0,
        y=620.0,
        width=100.0,
        height=100.0
    )
    #Input texts
    entry_image_1_intervalos = PhotoImage(
        file=relative_to_assets("entry_1_intervalos.png"))
    
    entry_bg_1_intervalos = canvas_intervalos.create_image(
        539.5,
        688.5,
        image=entry_image_1_intervalos
    )
    entry_1_intervalos = Entry(medicionEnIntervalos,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1_intervalos.place(
        x=508.0,
        y=673.0,
        width=63.0,
        height=29.0
    )
    
    entry_image_2_intervalos = PhotoImage(
        file=relative_to_assets("entry_2_intervalos.png"))
    entry_bg_2_intervalos = canvas_intervalos.create_image(
        841.5,
        685.5,
        image=entry_image_2_intervalos
    )
    entry_2_intervalos = Entry(medicionEnIntervalos,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_2_intervalos.place(
        x=810.0,
        y=670.0,
        width=63.0,
        height=29.0
    )
    #Header
    canvas_intervalos.create_text(
        363.0,
        28.0,
        anchor="nw",
        text="Medición En Intervalos",
        fill="#000000",
        font=("NunitoSans Regular", 40 * -1)
    )
    
    
    ##### Medicion Continua Widgets ####
    #Fondo
    canvasContinua = Canvas(
        medicionContinua,
        bg = "#FFFFFF",
        height = 720,
        width = 1280,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvasContinua.pack()
    #Imagenes
    image_image_1_continua = PhotoImage(
        file=relative_to_assets("image_1_Continua.png"))
    image_1_continua = canvasContinua.create_image(
        641.0,
        141.0,
        image=image_image_1_continua
    )
    
    image_image_2_continua = PhotoImage(
        file=relative_to_assets("image_2_Continua.png"))
    image_2_continua = canvasContinua.create_image(
        641.0,
        253.0,
        image=image_image_2_continua 
    )
    
    image_image_3_continua = PhotoImage(
        file=relative_to_assets("image_3_Continua.png"))
    image_3_continua = canvasContinua.create_image(
        637.0,
        365.0,
        image=image_image_3_continua
    )
    
    image_image_4_continua = PhotoImage(
        file=relative_to_assets("image_4_Continua.png"))
    image_4_continua = canvasContinua.create_image(
        637.0,
        477.0,
        image=image_image_4_continua
    )
    
    image_image_5_continua = PhotoImage(
        file=relative_to_assets("image_5_Continua.png"))
    image_5_continua = canvasContinua.create_image(
        637.0,
        589.0,
        image=image_image_5_continua
    )
    
    image_image_6_continua = PhotoImage(
        file=relative_to_assets("image_6_Continua.png"))
    image_6_continua = canvasContinua.create_image(
        57.0,
        87.0,
        image=image_image_6_continua
    )
    
    image_image_7_continua = PhotoImage(
        file=relative_to_assets("image_7_Continua.png"))
    image_7_continua = canvasContinua.create_image(
        1205.0,
        67.0,
        image=image_image_7_continua
    )
    
    image_image_8_continua = PhotoImage(
        file=relative_to_assets("image_8_Continua.png"))
    image_8_continua = canvasContinua.create_image(
        607.0,
        680.0,
        image=image_image_8_continua
    )
    #Texto
    pHText_continua=canvasContinua.create_text(
        332.0,
        123.0,
        anchor="nw",
        text="pH: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )

    conductividadText_continua=canvasContinua.create_text(
        332.0,
        235.0,
        anchor="nw",
        text="Conductividad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    temperaturaText_continua=canvasContinua.create_text(
        328.0,
        347.0,
        anchor="nw",
        text="Temperatura: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    indiceText_continua=canvasContinua.create_text(
        328.0,
        459.0,
        anchor="nw",
        text="Índice de Calidad de Agua: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    calidadText_continua=canvasContinua.create_text(
        328.0,
        571.0,
        anchor="nw",
        text="Calidad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
# Se definen las funciones
    def actualizarDatosContinua():
        #Hace una sola medicion de todas las variables.
        mediciones_continua = poll_sensors(sensor1, sensor2, usbports[0], usbports[1])
        print("Tiempo:", mediciones_continua['tiempo'])
        print("Temperatura:", mediciones_continua['temperatura'])
        print("Conductividad eléctrica:", mediciones_continua['conductividad_electrica'])
        print("pH:", mediciones_continua['pH'])
        print("Oxígeno disuelto:", mediciones_continua['oxigeno_disuelto'])
        print("Índice:", mediciones_continua['indice'])
        print("Calidad:", mediciones_continua['calidad'])

        pHValor_continua = mediciones_continua['pH']
        canvasContinua.itemconfig(tagOrId=pHText_continua, text=f"ph: {pHValor_continua}")

        conductividadValor_continua = mediciones_continua['conductividad_electrica']
        canvasContinua.itemconfig(tagOrId=conductividadText_continua, text=f"Conductividad: {conductividadValor_continua}")

        temperaturaValor_continua = mediciones_continua['temperatura']
        canvasContinua.itemconfig(tagOrId=temperaturaText_continua, text=f"Temperatura: {temperaturaValor_continua}")

        indice_continua = mediciones_continua['indice']
        canvasContinua.itemconfig(tagOrId=indiceText_continua, text=f"Índice de Calidad de Agua: {indice_continua}")

        calidad_continua = mediciones_continua['calidad']
        canvasContinua.itemconfig(tagOrId=calidadText_continua, text=calidad_continua)

    tiempo_muestreo_continua=1 #Tiempo default de 1 segundo

    def setTiempoMuestreo():
        global tiempo_muestreo_continua 
        tiempo_muestreo_continua= entry_1_continua.get()
        print(f"you set the sample time to {tiempo_muestreo_continua}")
        pass
    #Mide continuamente hasta que se presiona el boton detener  
    def medirContinuamenteContinua():
        global detener_continua
        detener_continua = False
        global tiempo_muestreo_continua
        while not detener_continua:
            actualizarDatosContinua()
            time.sleep(tiempo_muestreo_continua)  # Tiempo de muestreo en segs.
    #Detiene la medicio continua
    def detenerMedicionesContinua():
        global detener_continua
        detener_continua = True
        print("Detenido")
    

    #Botones
    button_image_1_continua = PhotoImage(
        file=relative_to_assets("button_1_Continua.png"))
    button_1_continua = Button(
        medicionContinua,
        image=button_image_1_continua,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:threading.Thread(target=medirContinuamenteContinua).start(), # Se crea un hilo dedicado a medir continuamente
        relief="flat"
    )
    button_1_continua.place(
        x=116.0,
        y=297.0,
        width=143.0,
        height=92.0
    )
    
    button_image_2_continua = PhotoImage(
        file=relative_to_assets("button_2_Continua.png"))
    button_2_continua = Button(
        medicionContinua,
        image=button_image_2_continua,
        borderwidth=0,
        highlightthickness=0,
        command=detenerMedicionesContinua,
        relief="flat"
    )
    button_2_continua.place(
        x=116.0,
        y=401.0,
        width=143.0,
        height=92.0
    )
    
    button_image_3_continua = PhotoImage(
        file=relative_to_assets("button_3_Continua.png"))
    button_3_continua = Button(
        medicionContinua,
        image=button_image_3_continua,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3_continua clicked"),
        relief="flat"
    )
    button_3_continua.place(
        x=1027.0,
        y=297.0,
        width=143.0,
        height=92.0
    )
    
    button_image_4_continua = PhotoImage(
        file=relative_to_assets("button_4_Continua.png"))
    button_4_continua = Button(
        medicionContinua,
        image=button_image_4_continua,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_4_continua clicked"),
        relief="flat"
    )
    button_4_continua.place(
        x=1027.0,
        y=401.0,
        width=143.0,
        height=92.0
    )
    
    button_image_5_continua = PhotoImage(
        file=relative_to_assets("button_5_Continua.png"))
    button_5_continua = Button(
        medicionContinua,
        image=button_image_5_continua,
        borderwidth=0,
        highlightthickness=0,
        command=setTiempoMuestreo, #boton ok para el muestreo
        relief="flat"
    )
    button_5_continua.place(
        x=894.0,
        y=651.0,
        width=60.0,
        height=59.0
    )
    
    button_image_6_continua = PhotoImage(
        file=relative_to_assets("button_6_Continua.png"))
    button_6_continua = Button(
        medicionContinua,
        image=button_image_6_continua,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_frame(Homescreen),  #Home
        relief="flat"
    )
    button_6_continua.place(
        x=1180.0,
        y=620.0,
        width=100.0,
        height=100.0
    )
    #Input text
    entry_image_1_continua = PhotoImage(
        file=relative_to_assets("entry_1_Continua.png"))
    
    entry_bg_1_continua = canvasContinua.create_image(
        746.0,
        684.5,
        image=entry_image_1_continua
    )
    entry_1_continua = Entry(
        medicionContinua,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1_continua.place(
        x=689.0,
        y=669.0,
        width=114.0,
        height=29.0
    )
    #Header
    canvasContinua.create_text(
        474.0,
        28.0,
        anchor="nw",
        text="Medición Continua",
        fill="#000000",
        font=("NunitoSans Regular", 40 * -1)
    )
    ###
    
    ##### Medicion Puntual Widgets ####
    #Fondo
    canvasPuntual = Canvas(
        medicionPuntual,
        bg = "#FFFFFF",
        height = 720,
        width = 1280,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvasPuntual.pack()
    
    #Imagenes
    image_image_1_puntual = PhotoImage(
        file=relative_to_assets("image_1_puntual.png"))
    image_1_puntual = canvasPuntual.create_image(
        641.0,
        179.0,
        image=image_image_1_puntual
    )
    image_image_2_puntual = PhotoImage(
        file=relative_to_assets("image_2_puntual.png"))
    image_2_puntual = canvasPuntual.create_image(
        641.0,
        291.0,
        image=image_image_2_puntual
    )
    
    image_image_3_puntual = PhotoImage(
        file=relative_to_assets("image_3_puntual.png"))
    image_3 = canvasPuntual.create_image(
        637.0,
        403.0,
        image=image_image_3_puntual
    )
    
    image_image_4_puntual = PhotoImage(
        file=relative_to_assets("image_4_puntual.png"))
    image_4 = canvasPuntual.create_image(
        637.0,
        515.0,
        image=image_image_4_puntual
    )
    
    image_image_5_puntual = PhotoImage(
        file=relative_to_assets("image_5_puntual.png"))
    image_5_puntual = canvasPuntual.create_image(
        637.0,
        627.0,
        image=image_image_5_puntual
    )
    
    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6_puntual.png"))
    image_6_puntual = canvasPuntual.create_image(
        57.0,
        87.0,
        image=image_image_6
    )
    
    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7_puntual.png"))
    image_7_puntual = canvasPuntual.create_image(
        1205.0,
        67.0,
        image=image_image_7
    )
    #Texto
    pHText_puntual=canvasPuntual.create_text(
        332.0,
        161.0,
        anchor="nw",
        text="pH: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    conductividadText_puntual=canvasPuntual.create_text(
        332.0,
        273.0,
        anchor="nw",
        text="Conductividad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    temperaturaText_puntual=canvasPuntual.create_text(
        328.0,
        385.0,
        anchor="nw",
        text="Temperatura: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    indiceText_puntual=canvasPuntual.create_text(
        328.0,
        497.0,
        anchor="nw",
        text="Índice de Calidad de Agua: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
    
    calidadText_puntual=canvasPuntual.create_text(
        328.0,
        609.0,
        anchor="nw",
        text="Calidad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 32 * -1)
    )
# Se definen las funciones
    def actualizarDatosPuntual():
        #Hace una sola medicion de todas las variables.
        mediciones_puntual = poll_sensors(sensor1, sensor2, usbports[0], usbports[1])
        print("Tiempo:", mediciones_puntual['tiempo'])
        print("Temperatura:", mediciones_puntual['temperatura'])
        print("Conductividad eléctrica:", mediciones_puntual['conductividad_electrica'])
        print("pH:", mediciones_puntual['pH'])
        print("Oxígeno disuelto:", mediciones_puntual['oxigeno_disuelto'])
        print("Índice:", mediciones_puntual['indice'])
        print("Calidad:", mediciones_puntual['calidad'])

        pHValor_puntual = mediciones_puntual['pH']
        canvasPuntual.itemconfig(tagOrId=pHText_puntual, text=f"ph: {pHValor_puntual}")

        conductividadValor_puntual = mediciones_puntual['conductividad_electrica']
        canvasPuntual.itemconfig(tagOrId=conductividadText_puntual, text=f"Conductividad: {conductividadValor_puntual}")

        temperaturaValor_puntual = mediciones_puntual['temperatura']
        canvasPuntual.itemconfig(tagOrId=temperaturaText_puntual, text=f"Temperatura: {temperaturaValor_puntual}")

        indice_puntual = mediciones_puntual['indice']
        canvasPuntual.itemconfig(tagOrId=indiceText_puntual, text=f"Índice de Calidad de Agua: {indice_puntual}")

        calidad = mediciones_puntual['calidad']
        canvasPuntual.itemconfig(tagOrId=calidadText_puntual, text=calidad)

    #Botones
    button_image_1_puntual = PhotoImage(
        file=relative_to_assets("button_1_puntual.png"))
    button_1_puntual = Button(
        medicionPuntual,
        image=button_image_1_puntual,
        borderwidth=0,
        highlightthickness=0,
        command=actualizarDatosPuntual, #Hace una lectura
        relief="flat"
    )
    button_1_puntual.place(
        x=116.0,
        y=297.0,
        width=143.0,
        height=92.0
    )
    
    button_image_2_puntual = PhotoImage(
        file=relative_to_assets("button_2_puntual.png"))
    button_2_puntual = Button(
        medicionPuntual,
        image=button_image_2_puntual,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_frame(Homescreen),  #Home
        relief="flat"
    )
    button_2_puntual.place(
        x=1180.0,
        y=620.0,
        width=100.0,
        height=100.0
    )
    #Header text
    canvasPuntual.create_text(
        485.0,
        28.0,
        anchor="nw",
        text="Medición Puntual",
        fill="#000000",
        font=("NunitoSans Regular", 40 * -1)
    )
    ###
    
    # Create the Homescreen frame
    Homescreen = Frame(window)
    Homescreen.grid(row=0, column=0)
    
    # Create a canvas within the Homescreen frame
    canvasHomescreen = Canvas(
        Homescreen,
        bg="#FFFFFF",
        height=720,
        width=1280,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvasHomescreen.pack()
    
    # Create buttons within the Homescreen frame
    button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
    button_1 = Button(
        Homescreen,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_frame(medicionPuntual),  # Switch to medicionPuntual frame
        relief="flat"
    )
    button_1.place(
        x=63.0,
        y=331.0,
        width=369.0,
        height=92.0
    )
    
    button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
    button_2 = Button(
        Homescreen,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_frame(medicionContinua),  # Switch 
        relief="flat"
    )
    button_2.place(
        x=444.0,
        y=331.0,
        width=369.0,
        height=92.0
    )
    
    button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
    button_3 = Button(
        Homescreen,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: show_frame(medicionEnIntervalos),  # Switch 
        relief="flat"
    )
    button_3.place(
        x=825.0,
        y=328.0,
        width=391.0,
        height=98.0
    )
    
    # Create images within the canvas
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvasHomescreen.create_image(
        57.0,
        87.0,
        image=image_image_1
    )
    
    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvasHomescreen.create_image(
        1205.0,
        67.0,
        image=image_image_2
    )
    
    # Header
    canvasHomescreen.create_text(
        346.0,
        28.0,
        anchor="nw",
        text="Sistema de Adquisición de Datos",
        fill="#000000",
        font=("NunitoSans Regular", 40 * -1)
    )
    
    window.resizable(False, False)
    window.mainloop()