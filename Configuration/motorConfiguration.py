import sys
sys.path.append("..")
from Enumerations import *

import serial
import time
import configparser
import menuGenerator

config = configparser.RawConfigParser()
config.read('../config.cfg')

def motorPorts():
	pass

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

