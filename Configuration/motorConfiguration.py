import sys
sys.path.append("..")
from Enumerations import *

import serial
import time
import configparser
import menuGenerator

#used for detecting key presses
import tty
import sys
import termios

config = configparser.RawConfigParser()
config.read('../config.cfg')

Motors = ["Left  " + name[0] for name in ArmParts.__members__.items()]
Motors += ["Right " + name[0] for name in ArmParts.__members__.items()]
Motors += ["Left  " + name[0] for name in LegParts.__members__.items()]
Motors += ["Right " + name[0] for name in LegParts.__members__.items()]

serialPort = serial.Serial("/dev/ttyUSB1", 115200, timeout=1)

def motorPorts():
	motorSelector = menuGenerator.menu("Which Motor?", ["None"] + Motors)
	print("A motor will be homed then moved. Select which motor has been moved. Press Q or q to quit.")
	for port in range(0,32):
		sendString = chr(35) + str(port) + " P" + str(1300) + " S" + str(500)
		serialPort.write((sendString + " \r").encode())
		time.sleep(3)
		sendString = chr(35) + str(port) + " P" + str(1700) + " S" + str(500)
		serialPort.write((sendString + " \r").encode())
		result = motorSelector.display(False)
		if result != "None":
			if result == "Back":
				return
			side = result[:5]
			if side == "Left ":
				side = Side.Left
			else:
				side = Side.Right
			result = result[6:]
			if result in [name[0] for name in ArmParts.__members__.items()]:
				motor = ArmParts[result]
			else:
				motor = LegParts[result]
			config['motors'][side.value + motor.value + "port"] = str(port)
			with open('../config.cfg', 'w') as configfile:
				config.write(configfile)
		


def motorHome():
	menu = menuGenerator.menu("Which Limb?", ["Arms", "Legs", "Both"])
	result = menu.display()
	while result != "Back":
		motorPorts = []
		if result == "Arms":
			for side in Side:
				motorPorts += [(config["motors"][side.value + part.value + "port"], side.value + part.value) for part in ArmParts]
		elif result == "Legs":
			for side in Side:
				motorPorts += [(config["motors"][side.value + part.value + "port"], side.value + part.value) for part in LegParts]
		elif result == "Both":
			for side in Side:
				motorPorts += [(config["motors"][side.value + part.value + "port"], side.value + part.value) for part in ArmParts]
			for side in Side:
				motorPorts += [(config["motors"][side.value + part.value + "port"], side.value + part.value) for part in LegParts]

		for motor in motorPorts:
			port = motor[0]
			print("Adjust value until motor is homed. Pres 'aaa' to set value.")
			print(motor[1])
			orig_settings = termios.tcgetattr(sys.stdin)

			tty.setraw(sys.stdin)
			x = 0
			counter = int(config["motors"][motor[1] + "home"])
			increment = 256
			previous = counter
			while x != "aaa": # ESC
				x=sys.stdin.read(3)
				if x == '\x1b[A':
					counter += increment
				if x == '\x1b[B':
					counter += -increment
				if x == '\x1b[C':
					increment = increment * 2
					print("Increment now: " + str(increment))
				if x == '\x1b[D':
					if increment > 1:
						increment = increment / 2
						print("Increment now: " + str(increment))
				if counter != previous:
					sendString = chr(35) + str(port) + " P" + str(counter) + " S" + str(500)
					print(counter)
					serialPort.write((sendString + " \r").encode())
				previous = counter

			termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
			print()
			config['motors'][motor[1] + "home"] = str(int(counter))
			with open('../config.cfg', 'w') as configfile:
                                config.write(configfile)
			time.sleep(1)

		result = menu.display(False)

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

