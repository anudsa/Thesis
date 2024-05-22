from pathlib import Path
from tkinter import *
from tkinter import messagebox
import serial
import sys
import time
import os
import re
import RPi.GPIO as GPIO
import mysql.connector
from datetime import datetime
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage 
import threading	
import exportar
import graficar
#import WQIFormula as WQI
import Formula
#Path para la gui es establecido
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/home/pi/Tesis/Thesis/Code/GUI/Homescreen/build/assets/smallframe0")
	
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
    #P=WQI.parametrizacion(conductividad,temp,potencialHidrogeno)
    #indice = WQI.calculo(P,[1,2,3])
    indice = Formula.calcular_indice(conductividad,temp,potencialHidrogeno)
    mediciones['indice'] = indice
    #calidad=WQI.interpretacion(indice)
    calidad = Formula.interpretacion(indice)
    mediciones['calidad'] = calidad
    addData(mediciones)
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

def leeUltimoid():
    # Consulta para encontrar el ID de la última fila de las lecturas
    cursor.execute("SELECT MAX(id) FROM lecturas")
    # Obtener el resultado
    resultado = cursor.fetchone()
    # Extraer el ID del resultado
    ultimo_id = int(resultado[0])
    return ultimo_id


#Function to add data
def addData(Data):
    # Create the INSERT query
    insert_query = "INSERT INTO lecturas (tiempo, temperatura, pH, conductividad, indice, calidad) VALUES (%s, %s, %s, %s, %s, %s)"
    # Execute the INSERT query with the values
    cursor.execute(insert_query, (Data['tiempo'], Data['temperatura'], Data['pH'], Data['conductividad_electrica'], Data['indice'], Data['calidad']))
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
    window.geometry("976x549")
    
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
        height = 549,
        width = 976,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas_intervalos.pack()
    #Imagenes
    image_image_1_intervalos = PhotoImage(
        file=relative_to_assets("image_1_intervalos.png"))
    image_1_intervalos = canvas_intervalos.create_image(
        488.8125,
        107.4375,
        image=image_image_1_intervalos
    )
    
    image_image_2_intervalos = PhotoImage(
        file=relative_to_assets("image_2_intervalos.png"))
    image_2_intervalos = canvas_intervalos.create_image(
        488.8125,
        192.8375244140625,
        image=image_image_2_intervalos
    )
    
    image_image_3_intervalos = PhotoImage(
        file=relative_to_assets("image_3_intervalos.png"))
    image_3_intervalos = canvas_intervalos.create_image(
        485.76251220703125,
        278.237548828125,
        image=image_image_3_intervalos
    )
    
    image_image_4_intervalos = PhotoImage(
        file=relative_to_assets("image_4_intervalos.png"))
    image_4_intervalos = canvas_intervalos.create_image(
        485.76251220703125,
        363.637451171875,
        image=image_image_4_intervalos
    )
    
    image_image_5_intervalos = PhotoImage(
        file=relative_to_assets("image_5_intervalos.png"))
    image_5_intervalos = canvas_intervalos.create_image(
        485.76251220703125,
        449.0374755859375,
        image=image_image_5_intervalos
    )
    
    image_image_6_intervalos = PhotoImage(
        file=relative_to_assets("image_6_intervalos.png"))
    image_6_intervalos = canvas_intervalos.create_image(
        44.0,
        66.0,
        image=image_image_6_intervalos
    )
    
    image_image_7_intervalos = PhotoImage(
        file=relative_to_assets("image_7_intervalos.png"))
    image_7_intervalos = canvas_intervalos.create_image(
        918.625,
        51.0,
        image=image_image_7_intervalos
    )
    
    image_image_8_intervalos = PhotoImage(
        file=relative_to_assets("image_8_intervalos.png"))
    image_8_intervalos = canvas_intervalos.create_image(
        347.7874755859375,
        521.4375,
        image=image_image_8_intervalos
    )
    
    image_image_9_intervalos = PhotoImage(
        file=relative_to_assets("image_9_intervalos.png"))
    image_9_intervalos = canvas_intervalos.create_image(
        598.4749755859375,
        521.4375,
        image=image_image_9_intervalos
    )
    #Texto
    pHText_intervalos=canvas_intervalos.create_text(
        253.1500244140625,
        93.7874755859375,
        anchor="nw",
        text="pH: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    conductividadText_intervalos=canvas_intervalos.create_text(
        253.1500244140625,
        179.1875,
        anchor="nw",
        text="Conductividad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    temperaturaText_intervalos=canvas_intervalos.create_text(
        250.0999755859375,
        264.5875244140625,
        anchor="nw",
        text="Temperatura: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    indiceText_intervalos=canvas_intervalos.create_text(
        250.0999755859375,
        349.987548828125,
        anchor="nw",
        text="Índice de Calidad de Agua: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    calidadText_intervalos=canvas_intervalos.create_text(
        250.0999755859375,
        435.387451171875,
        anchor="nw",
        text="Calidad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )

    # Se definen las funciones
    def actualizarDatosIntervalos():
        #Hace una sola medicion de todas las variables (la cual se guarda en la base de datos)
        mediciones_intervalos = poll_sensors(sensor1, sensor2, usbports[0], usbports[1])
        
        pHValor_intervalos = mediciones_intervalos['pH']
        canvas_intervalos.itemconfig(tagOrId=pHText_intervalos, text=f"pH: {pHValor_intervalos:.4f}")

        conductividadValor_intervalos = mediciones_intervalos['conductividad_electrica']
        canvas_intervalos.itemconfig(tagOrId=conductividadText_intervalos, text=f"Conductividad: {conductividadValor_intervalos:.4f}")

        temperaturaValor_intervalos = mediciones_intervalos['temperatura']
        canvas_intervalos.itemconfig(tagOrId=temperaturaText_intervalos, text=f"Temperatura: {temperaturaValor_intervalos:.4f}")

        indice_intervalos = mediciones_intervalos['indice']
        canvas_intervalos.itemconfig(tagOrId=indiceText_intervalos, text=f"Índice de Calidad de Agua: {indice_intervalos:.4f}")

        calidad_intervalos = mediciones_intervalos['calidad']
        canvas_intervalos.itemconfig(tagOrId=calidadText_intervalos, text=f"Calidad: {calidad_intervalos}")

    tiempo_muestreo_intervalos=1 #Tiempo default de 1 segundo
    duracion_intervalos=5 #Tiempo default de 5 segundos

    def setTiempos():
        global tiempo_muestreo_intervalos
        global duracion_intervalos
        try:
            tiempo_muestreo_intervalos = int(entry_1_intervalos.get())
            duracion_intervalos = int(entry_2_intervalos.get())
            #Se verifica que el tiempo de muestreo sea menor a la duración
            if(duracion_intervalos<tiempo_muestreo_intervalos):
                messagebox.showerror("Error","El tiempo de muestreo debe ser menor a la duración total")  
            elif(tiempo_muestreo_intervalos==0 or duracion_intervalos==0):
                messagebox.showerror("Error","Inserte un valor mayor a cero")
            #Limita el tiempo máximo a 1 año en ambos casos
            elif(duracion_intervalos<31536000 and tiempo_muestreo_intervalos<31536000):
                messagebox.showinfo("Listo",f"La duración total es {duracion_intervalos}s y el tiempo de muestreo es de {tiempo_muestreo_intervalos}s.")
        except ValueError:
            messagebox.showerror("Error","Inserte datos válidos")

    detener_intervalos=False
    
    def medirEnIntervalos(tiempo_muestreo_intervalos, duracion_intervalos):
        messagebox.showinfo("","Medición iniciada.")
        if duracion_intervalos < tiempo_muestreo_intervalos or duracion_intervalos <=0 or tiempo_muestreo_intervalos <= 0:
            messagebox.showerror("Error","Inserte datos válidos")
            return
        global id_inicial_intervalos
        id_inicial_intervalos=leeUltimoid()+1
        global id_final_intervalos
        global detener_intervalos
        detener_intervalos=False
        offset_inicial=0
        tiempo_transcurrido = 0
        tiempo_inicio = time.time()
        for i in range(duracion_intervalos // tiempo_muestreo_intervalos +1):
            actualizarDatosIntervalos()
            tiempo_transcurrido = time.time() - tiempo_inicio
            if  tiempo_transcurrido<=0.9:
                offset_inicial=tiempo_transcurrido
            #print("Tiempo transcurrido:", tiempo_transcurrido)
            if  detener_intervalos==True:
                break
            time.sleep(tiempo_muestreo_intervalos-offset_inicial)
        print("Tiempo total:", tiempo_transcurrido)
        id_final_intervalos=leeUltimoid()
        messagebox.showinfo("Listo","El intervalo ha terminado.")

    #Regresa a home y detiene mediciones
    def irAHomeIntervalos():
        global detener_intervalos
        detener_intervalos=True
        show_frame(Homescreen)
    
    #Funcion para graficar
    def graficarIntervalos():
        global id_inicial_intervalos
        global id_final_intervalos
        graficar.graficarDatos(id_inicial_intervalos,id_final_intervalos)

    #Funcion para exportar a Excel
    def exportarIntervalos():
        exportar.exportarExcel(id_inicial_intervalos,id_final_intervalos)
        messagebox.showinfo("Listo","Se ha guardado en la ruta /home/pi/Desktop/ArchivosExportados/")

    #Botones
    button_image_1_intervalos = PhotoImage(
        file=relative_to_assets("button_1_intervalos.png"))
    button_1_intervalos = Button(medicionEnIntervalos,
        image=button_image_1_intervalos,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: threading.Thread(target=lambda: medirEnIntervalos(tiempo_muestreo_intervalos, duracion_intervalos)).start(), # Se crea un hilo dedicado a medir continuamente
        relief="flat"
    )
    button_1_intervalos.place(
        x=88.45001220703125,
        y=226.4625244140625,
        width=109.03750610351562,
        height=70.14999389648438
    )
    
    button_image_2_intervalos = PhotoImage(
        file=relative_to_assets("button_2_intervalos.png"))
    button_2_intervalos = Button(medicionEnIntervalos,
        image=button_image_2_intervalos,
        borderwidth=0,
        highlightthickness=0,
        command=graficarIntervalos, #Graficar
        relief="flat"
    )
    button_2_intervalos.place(
        x=783.0875244140625,
        y=226.4625244140625,
        width=109.03750610351562,
        height=70.14999389648438
    )
    
    button_image_3_intervalos = PhotoImage(
        file=relative_to_assets("button_3_intervalos.png"))
    button_3_intervalos = Button(medicionEnIntervalos,
        image=button_image_3_intervalos,
        borderwidth=0,
        highlightthickness=0,
        command=exportarIntervalos, #Exportar
        relief="flat"
    )
    button_3_intervalos.place(
        x=783.0875244140625,
        y=305.762451171875,
        width=109.03750610351562,
        height=70.14999389648438
    )
    
    button_image_4_intervalos = PhotoImage(
        file=relative_to_assets("button_4_intervalos.png"))
    button_4_intervalos = Button(medicionEnIntervalos,
        image=button_image_4_intervalos,
        borderwidth=0,
        highlightthickness=0,
        command=setTiempos, #Boton "OK"
        relief="flat"
    )
    button_4_intervalos.place(
        x=719.0374755859375,
        y=499.4375,
        width=45.75,
        height=44.98750305175781
    )
    
    button_image_5_intervalos = PhotoImage(
        file=relative_to_assets("button_5_intervalos.png"))
    button_5_intervalos = Button(medicionEnIntervalos,
        image=button_image_5_intervalos,
        borderwidth=0,
        highlightthickness=0,
        command=irAHomeIntervalos, #Home 
        relief="flat"
    )
    button_5_intervalos.place(
        x=899.75,
        y=472.75,
        width=76.25,
        height=76.25
    )
    #Input texts
    entry_image_1_intervalos = PhotoImage(
        file=relative_to_assets("entry_1_intervalos.png"))
    
    entry_bg_1_intervalos = canvas_intervalos.create_image(
        411.3687286376953,
        524.9812259674072,
        image=entry_image_1_intervalos
    )
    entry_1_intervalos = Entry(medicionEnIntervalos,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_1_intervalos.place(
        x=387.3499755859375,
        y=513.1624755859375,
        width=48.037506103515625,
        height=21.637500762939453
    )
    
    entry_image_2_intervalos = PhotoImage(
        file=relative_to_assets("entry_2_intervalos.png"))
    entry_bg_2_intervalos = canvas_intervalos.create_image(
        641.6437530517578,
        522.6937503814697,
        image=entry_image_2_intervalos
    )
    entry_2_intervalos = Entry(medicionEnIntervalos,
        bd=0,
        bg="#FFFFFF",
        fg="#000716",
        highlightthickness=0
    )
    entry_2_intervalos.place(
        x=617.625,
        y=510.875,
        width=48.037506103515625,
        height=21.637500762939453
    )
    #Header
    canvas_intervalos.create_text(
        276.7874755859375,
        21.3499755859375,
        anchor="nw",
        text="Medición En Intervalos",
        fill="#000000",
        font=("NunitoSans Regular", 30 * -1)
    )
    
    
    ##### Medicion Continua Widgets ####
    #Fondo
    canvasContinua = Canvas(
        medicionContinua,
        bg = "#FFFFFF",
        height = 549,
        width = 976,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvasContinua.pack()
    #Imagenes
    image_image_1_continua = PhotoImage(
        file=relative_to_assets("image_1_Continua.png"))
    image_1_continua = canvasContinua.create_image(
        488.8125,
        107.4375,
        image=image_image_1_continua
    )
    
    image_image_2_continua = PhotoImage(
        file=relative_to_assets("image_2_Continua.png"))
    image_2_continua = canvasContinua.create_image(
        488.8125,
        192.83749389648438,
        image=image_image_2_continua 
    )
    
    image_image_3_continua = PhotoImage(
        file=relative_to_assets("image_3_Continua.png"))
    image_3_continua = canvasContinua.create_image(
        485.76251220703125,
        278.23748779296875,
        image=image_image_3_continua
    )
    
    image_image_4_continua = PhotoImage(
        file=relative_to_assets("image_4_Continua.png"))
    image_4_continua = canvasContinua.create_image(
        485.76251220703125,
        363.6375732421875,
        image=image_image_4_continua
    )
    
    image_image_5_continua = PhotoImage(
        file=relative_to_assets("image_5_Continua.png"))
    image_5_continua = canvasContinua.create_image(
        485.76251220703125,
        449.0374755859375,
        image=image_image_5_continua
    )
    
    image_image_6_continua = PhotoImage(
        file=relative_to_assets("image_6_Continua.png"))
    image_6_continua = canvasContinua.create_image(
        44.0,
        66.0,
        image=image_image_6_continua
    )
    
    image_image_7_continua = PhotoImage(
        file=relative_to_assets("image_7_Continua.png"))
    image_7_continua = canvasContinua.create_image(
        918.6250610351562,
        51.0,
        image=image_image_7_continua
    )
    
    image_image_8_continua = PhotoImage(
        file=relative_to_assets("image_8_Continua.png"))
    image_8_continua = canvasContinua.create_image(
        462.76251220703125,
        518.3875122070312,
        image=image_image_8_continua
    )
    #Texto
    pHText_continua=canvasContinua.create_text(
        253.14999389648438,
        93.78750610351562,
        anchor="nw",
        text="pH: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )

    conductividadText_continua=canvasContinua.create_text(
        253.14999389648438,
        179.18753051757812,
        anchor="nw",
        text="Conductividad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    temperaturaText_continua=canvasContinua.create_text(
        250.10003662109375,
        264.5875244140625,
        anchor="nw",
        text="Temperatura: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    indiceText_continua=canvasContinua.create_text(
        250.10003662109375,
        349.987548828125,
        anchor="nw",
        text="Índice de Calidad de Agua: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    calidadText_continua=canvasContinua.create_text(
        250.10003662109375,
        435.38751220703125,
        anchor="nw",
        text="Calidad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    # Se definen las funciones
    def actualizarDatosContinua():
        #Hace una sola medicion de todas las variables.
        mediciones_continua = poll_sensors(sensor1, sensor2, usbports[0], usbports[1])
        
        pHValor_continua = mediciones_continua['pH']
        canvasContinua.itemconfig(tagOrId=pHText_continua, text=f"pH: {pHValor_continua:.4f}")

        conductividadValor_continua = mediciones_continua['conductividad_electrica']
        canvasContinua.itemconfig(tagOrId=conductividadText_continua, text=f"Conductividad: {conductividadValor_continua:.4f}")

        temperaturaValor_continua = mediciones_continua['temperatura']
        canvasContinua.itemconfig(tagOrId=temperaturaText_continua, text=f"Temperatura: {temperaturaValor_continua:.4f}")

        indice_continua = mediciones_continua['indice']
        canvasContinua.itemconfig(tagOrId=indiceText_continua, text=f"Índice de Calidad de Agua: {indice_continua:.4f}")

        calidad_continua = mediciones_continua['calidad']
        canvasContinua.itemconfig(tagOrId=calidadText_continua, text=f"Calidad: {calidad_continua}")
 
    tiempo_muestreo_continua=1 #Tiempo default de 1 segundo

    def setTiempoMuestreo():
        global tiempo_muestreo_continua 
        try:
            tiempo_muestreo_continua= int(entry_1_continua.get())
            if(tiempo_muestreo_continua==1):
                messagebox.showinfo("Listo",f"El tiempo de muestreo ahora es de {tiempo_muestreo_continua} segundo.")    
            elif(tiempo_muestreo_continua==0):
                messagebox.showerror("Error","Inserte un número válido")
            #Limita el tiempo máximo a 30 días
            elif(tiempo_muestreo_intervalos<2592000):
                messagebox.showinfo("Listo",f"El tiempo de muestreo ahora es de {tiempo_muestreo_continua} segundos.")
        except ValueError:
            messagebox.showerror("Error","Inserte un número válido")
    
    #Mide continuamente hasta que se presiona el boton detener  
    def medirContinuamente():
        messagebox.showinfo("","Medición iniciada.")
        global id_inicial_continua 
        id_inicial_continua = leeUltimoid()+1
        global detener_continua
        detener_continua = False
        global tiempo_muestreo_continua
        #If que limita el tiemo
        if (tiempo_muestreo_continua>0 and tiempo_muestreo_continua<2592000):
            while not detener_continua:
                actualizarDatosContinua()
                time.sleep(tiempo_muestreo_continua)  # Tiempo de muestreo en segs.
            messagebox.showinfo("","Detenido")

    #Detiene la medicion continua
    def detenerMedicionesContinua():
        global detener_continua
        detener_continua = True
        global id_final_continua
        id_final_continua = leeUltimoid()
        

    #Funcion para graficar
    def graficarcontinua():
        global id_inicial_continua
        global id_final_continua
        graficar.graficarDatos(id_inicial_continua,id_final_continua)

    #Funcion para exportar a Excel
    def exportarContinua():
        exportar.exportarExcel(id_inicial_continua,id_final_continua)
        messagebox.showinfo("Listo","Se ha guardado en la ruta /home/pi/Desktop/ArchivosExportados/")

    #Regresa a home y detiene mediciones
    def irAHomeContinua():
        detenerMedicionesContinua()
        show_frame(Homescreen)
       

    #Botones
    button_image_1_continua = PhotoImage(
        file=relative_to_assets("button_1_Continua.png"))
    button_1_continua = Button(
        medicionContinua,
        image=button_image_1_continua,
        borderwidth=0,
        highlightthickness=0,
        command=lambda:threading.Thread(target=medirContinuamente).start(), # Se crea un hilo dedicado a medir continuamente
        relief="flat"
    )
    button_1_continua.place(
        x=88.44999694824219,
        y=226.46246337890625,
        width=109.03750610351562,
        height=70.1500015258789
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
        x=88.44999694824219,
        y=305.762451171875,
        width=109.03750610351562,
        height=70.1500015258789
    )
    
    button_image_3_continua = PhotoImage(
        file=relative_to_assets("button_3_Continua.png"))
    button_3_continua = Button(
        medicionContinua,
        image=button_image_3_continua,
        borderwidth=0,
        highlightthickness=0,
        command=graficarcontinua, #Graficar
        relief="flat"
    )
    button_3_continua.place(
        x=783.0875244140625,
        y=226.46246337890625,
        width=109.03750610351562,
        height=70.1500015258789
    )
    
    button_image_4_continua = PhotoImage(
        file=relative_to_assets("button_4_Continua.png"))
    button_4_continua = Button(
        medicionContinua,
        image=button_image_4_continua,
        borderwidth=0,
        highlightthickness=0,
        command=exportarContinua, #Exportar
        relief="flat"
    )
    button_4_continua.place(
        x=783.0875244140625,
        y=305.762451171875,
        width=109.03750610351562,
        height=70.1500015258789
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
        x=681.675048828125,
        y=496.38751220703125,
        width=45.750003814697266,
        height=44.98750305175781
    )
    
    button_image_6_continua = PhotoImage(
        file=relative_to_assets("button_6_Continua.png"))
    button_6_continua = Button(
        medicionContinua,
        image=button_image_6_continua,
        borderwidth=0,
        highlightthickness=0,
        command=irAHomeContinua,  #Home
        relief="flat"
    )
    button_6_continua.place(
        x=899.75,
        y=472.75006103515625,
        width=76.25000762939453,
        height=76.25000762939453
    )
    #Input text
    entry_image_1_continua = PhotoImage(
        file=relative_to_assets("entry_1_Continua.png"))
    
    entry_bg_1_continua = canvasContinua.create_image(
        568.8249931335449,
        521.9311771392822,
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
        x=525.3624877929688,
        y=510.1124267578125,
        width=86.92501068115234,
        height=21.637500762939453
    )
    #Header
    canvasContinua.create_text(
        361.42498779296875,
        21.350006103515625,
        anchor="nw",
        text="Medición Continua",
        fill="#000000",
        font=("NunitoSans Regular", 30 * -1)
    )
    ###
    
    ##### Medicion Puntual Widgets ####
    #Fondo
    canvasPuntual = Canvas(
        medicionPuntual,
        bg = "#FFFFFF",
        height = 549,
        width = 976,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvasPuntual.pack()
    
    #Imagenes
    image_image_1_puntual = PhotoImage(
        file=relative_to_assets("image_1_puntual.png"))
    image_1_puntual = canvasPuntual.create_image(
        488.8125,
        136.41250610351562,
        image=image_image_1_puntual
    )
    image_image_2_puntual = PhotoImage(
        file=relative_to_assets("image_2_puntual.png"))
    image_2_puntual = canvasPuntual.create_image(
        488.8125,
        221.8125,
        image=image_image_2_puntual
    )
    
    image_image_3_puntual = PhotoImage(
        file=relative_to_assets("image_3_puntual.png"))
    image_3 = canvasPuntual.create_image(
        485.76251220703125,
        307.2125244140625,
        image=image_image_3_puntual
    )
    
    image_image_4_puntual = PhotoImage(
        file=relative_to_assets("image_4_puntual.png"))
    image_4 = canvasPuntual.create_image(
        485.76251220703125,
        392.61248779296875,
        image=image_image_4_puntual
    )
    
    image_image_5_puntual = PhotoImage(
        file=relative_to_assets("image_5_puntual.png"))
    image_5_puntual = canvasPuntual.create_image(
        485.76251220703125,
        478.01251220703125,
        image=image_image_5_puntual
    )
    
    image_image_6 = PhotoImage(
        file=relative_to_assets("image_6_puntual.png"))
    image_6_puntual = canvasPuntual.create_image(
        44.0,
        66.0,
        image=image_image_6
    )
    
    image_image_7 = PhotoImage(
        file=relative_to_assets("image_7_puntual.png"))
    image_7_puntual = canvasPuntual.create_image(
        918.625,
        51.0,
        image=image_image_7
    )
    #Texto
    pHText_puntual=canvasPuntual.create_text(
        253.14999389648438,
        122.76251220703125,
        anchor="nw",
        text="pH: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    conductividadText_puntual=canvasPuntual.create_text(
        253.14999389648438,
        208.16250610351562,
        anchor="nw",
        text="Conductividad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    temperaturaText_puntual=canvasPuntual.create_text(
        250.10000610351562,
        293.5625,
        anchor="nw",
        text="Temperatura: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    indiceText_puntual=canvasPuntual.create_text(
        250.10000610351562,
        378.9625244140625,
        anchor="nw",
        text="Índice de Calidad de Agua: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
    
    calidadText_puntual=canvasPuntual.create_text(
        250.10000610351562,
        464.36248779296875,
        anchor="nw",
        text="Calidad: N/A",
        fill="#FFFFFF",
        font=("NunitoSans Regular", 24 * -1)
    )
# Se definen las funciones
    def actualizarDatosPuntual():
        #Hace una sola medicion de todas las variables.
        mediciones_puntual = poll_sensors(sensor1, sensor2, usbports[0], usbports[1])

        pHValor_puntual = mediciones_puntual['pH']
        #canvasPuntual.itemconfig(tagOrId=pHText_puntual, text=f"pH: {pHValor_puntual}")
        canvasPuntual.itemconfig(tagOrId=pHText_puntual, text=f"pH: {pHValor_puntual:.4f}")


        conductividadValor_puntual = mediciones_puntual['conductividad_electrica']
        canvasPuntual.itemconfig(tagOrId=conductividadText_puntual, text=f"Conductividad: {conductividadValor_puntual:.4f}")

        temperaturaValor_puntual = mediciones_puntual['temperatura']
        canvasPuntual.itemconfig(tagOrId=temperaturaText_puntual, text=f"Temperatura: {temperaturaValor_puntual:.4f}")

        indice_puntual = mediciones_puntual['indice']
        canvasPuntual.itemconfig(tagOrId=indiceText_puntual, text=f"Índice de Calidad de Agua: {indice_puntual:.4f}")

        calidad = mediciones_puntual['calidad']
        canvasPuntual.itemconfig(tagOrId=calidadText_puntual, text=f"Calidad: {calidad}")

    #Regresa a home y detiene mediciones
    def irAHomePuntual():
        show_frame(Homescreen)
       
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
        x=88.44999694824219,
        y=226.46249389648438,
        width=109.0374984741211,
        height=70.1500015258789
    )
    
    button_image_2_puntual = PhotoImage(
        file=relative_to_assets("button_2_puntual.png"))
    button_2_puntual = Button(
        medicionPuntual,
        image=button_image_2_puntual,
        borderwidth=0,
        highlightthickness=0,
        command=irAHomePuntual,  #Home
        relief="flat"
    )
    button_2_puntual.place(
        x=899.75,
        y=472.75,
        width=76.25,
        height=76.25
    )
    #Header text
    canvasPuntual.create_text(
        369.8125,
        21.350006103515625,
        anchor="nw",
        text="Medición Puntual",
        fill="#000000",
        font=("NunitoSans Regular", 30 * -1)
    )
    ###
    
    # Create the Homescreen frame
    Homescreen = Frame(window)
    Homescreen.grid(row=0, column=0)
    
    # Create a canvas within the Homescreen frame
    canvasHomescreen = Canvas(
        Homescreen,
        bg="#FFFFFF",
        height=549,
        width=976,
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
        x=48.037506103515625,
        y=252.38763427734375,
        width=281.36248779296875,
        height=70.15000915527344
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
        x=338.54998779296875,
        y=252.38763427734375,
        width=281.36248779296875,
        height=70.15000915527344
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
        x=629.0625,
        y=250.0999755859375,
        width=298.1375732421875,
        height=74.7249984741211
    )
    
    # Create images within the canvas
    image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
    image_1 = canvasHomescreen.create_image(
        44.0,
        66.0,
        image=image_image_1
    )
    
    image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
    image_2 = canvasHomescreen.create_image(
        918.625,
        51.0,
        image=image_image_2
    )
    
    # Header
    canvasHomescreen.create_text(
        263.8250427246094,
        21.350006103515625,
        anchor="nw",
        text="Sistema de Adquisición de Datos",
        fill="#000000",
        font=("NunitoSans Regular", 30 * -1)
    )
    
    window.resizable(False, False)
    window.mainloop()