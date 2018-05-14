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

def __isInt(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def measure():
        """Measures the current reading of the battery. Returns a floating point number. Returns -1 if reading has failed"""
        ser.write("measure".encode())
        x = str(ser.readline())
        x = x[2:-5]
        if __isInt(x):
                x = float(x)
                return(x)
        return(-1)

def on():
        """Turns the battery power on. Will only turn on if safety relay has not previously been tripped"""
        ser.write("on".encode())
        print("on")

def off():
        """Turns the battery power off"""
        ser.write("off".encode())
        print("off")

def set(value):
        """Sets the trigger voltage of the safety cut off to the supplied value"""
        ser.write(("set" + str(value)).encode())
