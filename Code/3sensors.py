import serial
import sys
import time
import os
import re
import RPi.GPIO as GPIO

#function to get temperatures
def leerTemperatura():
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
        one_wire_temps = leerTemperatura()

        if one_wire_temps:
            print("Temperatura: {:.2f}°C".format(one_wire_temps[0]))
        else:
            print("Unable to read temperature from One-Wire Sensor.")

        send_cmd(sensor1, "R")
        lines1 = read_lines(sensor1)
        for i in range(len(lines1)):
            if lines1[i][0] != b'*'[0]:
                print("Conductividad {}: {}".format(usbport1, lines1[i].decode('utf-8')))

        send_cmd(sensor2, "R")
        lines2 = read_lines(sensor2)
        for i in range(len(lines2)):
            if lines2[i][0] != b'*'[0]:
                print("pH {}: {}".format(usbport2, lines2[i].decode('utf-8')))

        time.sleep(1)  #Tiempo de muestreo

if __name__ == "__main__":
    
    usbports = ['/dev/ttyUSB0', '/dev/ttyUSB1']

    try:
        sensor1 = serial.Serial(usbports[0], 9600, timeout=0)
    except serial.SerialException as e:
        print("Error al abrir el puerto serial {}: {}".format(usbports[0], e))
        sys.exit(1)

    try:
        sensor2 = serial.Serial(usbports[1], 9600, timeout=0)
    except serial.SerialException as e:
        print("Error al abrir el puerto serial {}: {}".format(usbports[1], e))
        sys.exit(1)

    poll_sensors(sensor1, sensor2, usbports[0], usbports[1])
