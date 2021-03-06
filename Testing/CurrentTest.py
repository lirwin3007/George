import time
import serial
import os          

if __name__ == "__main__":      
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

while __name__ == "__main__":
	ser.write("measure".encode())
	x = str(ser.readline())
	x = x[2:-5]
	if isInt(x):
		x = float(x)
		os.system("clear")
		print(x)
