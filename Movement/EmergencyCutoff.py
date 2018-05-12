import time
import serial
import os

ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

def isInt(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def measure():
        ser.write("measure".encode())
        x = str(ser.readline())
        x = x[2:-5]
        if isInt(x):
                x = float(x)
                return(x)
        return(0)

def on():
        ser.write("on".encode())
        print("on")

def off():
        ser.write("off".encode())
        print("off")

def set(value):
	ser.write(("set" + str(value)).encode())
