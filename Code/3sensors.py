import serial
import sys
import time
import os
import re
import RPi.GPIO as GPIO
#function to get temperatures
def getTemperatures():
    # returns a list of temperatures from all available "28*" onewire devices
    allTemps = list()
    onewire_basedir = "/sys/bus/w1/devices/"
    onewire_devices = os.listdir(onewire_basedir)
    onewire_retemp = re.compile('t=(\d*)')
    #Loop to find if the listed device is a sensor i.e. name starts with 28
    for device_string in onewire_devices:
        if device_string.startswith("28"):
            onewire_path = os.path.join(onewire_basedir, device_string, "w1_slave")
            onewire_devfile = open(onewire_path, "r")
            onewire_devtext = onewire_devfile.readlines()
            onewire_temp = onewire_retemp.search(onewire_devtext[1])
            #Conversion to display temp in C°
            temperature = int(onewire_temp.group(1)) / 1000.0
            allTemps.append(temperature)
    return allTemps

def read_line(sensor):
    # Function to read a line from the sensor
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
    # Function to read multiple lines from the sensor
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
    # Function to send a command to the Atlas Sensor
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
        # Read temperatures from DS18B20 one-wire sensor
        one_wire_temps = getTemperatures()

        # Print temperatures from the one-wire sensor
        if one_wire_temps:
            print("Temperature from One-Wire Sensor: {:.2f}°C".format(one_wire_temps[0]))
        else:
            print("Unable to read temperature from One-Wire Sensor.")

        # Poll the first sensor
        send_cmd(sensor1, "R")
        lines1 = read_lines(sensor1)
        for i in range(len(lines1)):
            if lines1[i][0] != b'*'[0]:
                print("Response from {}: {}".format(usbport1, lines1[i].decode('utf-8')))

        # Poll the second sensor
        send_cmd(sensor2, "R")
        lines2 = read_lines(sensor2)
        for i in range(len(lines2)):
            if lines2[i][0] != b'*'[0]:
                print("Response from {}: {}".format(usbport2, lines2[i].decode('utf-8')))

        time.sleep(1)  # Adjust as needed



if __name__ == "__main__":

    poll_sensors(sensor1, sensor2, usbports[0], usbports[1])
