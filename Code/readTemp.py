# read the ds18b20 one-wire temperature sensor
import RPi.GPIO as GPIO
import os
import re

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

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
#Infinite loop
try:
    while True:
        all_temps = getTemperatures()
        if all_temps:
            print("Temperatura: ", all_temps)
#Ctrl + c triggers this interrupt
except KeyboardInterrupt:
    print("Finalizado")

