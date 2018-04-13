import sys
sys.path.append("..")
from Enumerations import *

import serial
import time
import configparser
import menuGenerator

config = configparser.RawConfigParser()
config.read('../config.cfg')

Motors = ["Left  " + name[0] for name in ArmParts.__members__.items()]
Motors += ["Right " + name[0] for name in ArmParts.__members__.items()]
Motors += ["Left  " + name[0] for name in LegParts.__members__.items()]
Motors += ["Right " + name[0] for name in LegParts.__members__.items()]

serialPort = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)

def motorPorts():
	motorSelector = menuGenerator.menu("Which Motor?", ["None"] + Motors )
	print("A motor will be homed then moved. Select which motor has been moved. Press Q or q to quit.")
	for port in range(0,32):
		sendString = "\#" + str(port) + " P" + str(1500) + " S" + str(5)
		serialPort.write((sendString + " \r").encode())
		time.sleep(1)
		sendString = "\#" + str(port) + " P" + str(1700) + " S" + str(5)
		serialPort.write((sendString + " \r").encode())
		result = motorSelector.display()


def motorHome():
	print("Not Yet Implimented")

def minMax():
	print("Not Yet Implimented")


menu = menuGenerator.menu("Command line utility to configure motor ports, homes [NYI], maximums [NYI] and minimums [NYI]", ["Motor Ports", "Motor Home", "Motor Minimum and Maximum", "Run All"])

running = True
while running:
	choice = menu.display()

	if choice == "Motor Ports":
		motorPorts()
	elif choice == "Motor Home":
		motorHome()
	elif choice == "Motor Minimum and Maximum":
		minMax()
	elif choice == "Run All":
		motorPorts()
		motorHome()
		minMax()
	elif choice == "Quit":
		running = False
	else:
		print("Choice Error")

