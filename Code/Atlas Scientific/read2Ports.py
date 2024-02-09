import serial
import sys
import time

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
            sensor.flushInput()  # Use flushInput instead of flush_input
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

def poll_sensor(sensor, usbport):
    print("Polling sensor connected to {}: ".format(usbport))

    while True:
        send_cmd(sensor, "R")
        lines = read_lines(sensor)
        for i in range(len(lines)):
            if lines[i][0] != b'*'[0]:
                print("Response: {}".format(lines[i].decode('utf-8')))
        time.sleep(1)  # Adjust as needed

if __name__ == "__main__":
    usbports = ['/dev/ttyUSB0', '/dev/ttyUSB1']  # A list with the USB ports is created

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

    poll_sensor(sensor1, usbports[0])
    poll_sensor(sensor2, usbports[1])
