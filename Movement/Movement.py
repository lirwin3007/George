import sys
sys.path.append("..")
from Enumerations import *

import serial
import time
import configparser
import math

config = configparser.RawConfigParser()
config.read('../config.cfg')

class MotorMovement:
	def __init__(self, motors, positions, speeds = [],  positionType = MovementTypes.Angle):
		#validation
		if len(motors) != len(positions) or len(motors) == 0:
			raise Exception("Length of motors != length of positions")	

		#Self variable setting
		self.speeds = []
		if speeds == []:
			for motor in motors:
				self.speeds.append(config.getfloat('motors', motor.type.value + "speed"))
		elif len(speeds) != len(motors):
			print("WARNING: Number of speeds does not match number of motors. Setting all to default value")
			for motor in motors:
				self.speeds.append(config.getfloat('motors', motor.type.value + "speed"))
		else:
			self.speeds = speeds

		self.motors = motors
		if positionType == MovementTypes.Absolute:
			self.positions = positions
		elif positionType == MovementTypes.Angle:
			self.positions = []
			for counter in range(0, len(motors)):
				self.positions.append(motors[counter].angleToAbsolute(positions[counter]))
		elif positionType == MovementTypes.Percentage:
			self.positions = []
			for counter in range(0, len(motors)):
				self.positions.append(motors[counter].percentageToAbsolute(positions[counter]))

	def execute(self, port):
		sendString = ""
		for counter in range(0, len(self.motors)):
			sendString += str(unichr(35)) + str(self.motors[counter]) + " P" + str(self.positions[counter]) + " S" + str(self.speeds[counter])
		port.write(sendString + " \r")


class Motor:
	def __init__(self, port, type, home, max, min):
		self.port = port
		self.type = type
		self.home = home
		self.max = max
		self.min = min

	def angleToAbsolute(self, degree):
		stepPerDegree = config.getfloat('motors', self.type.value + "stepperdegree")
		absolute = self.home + degree * stepPerDegree
		if absolute > self.max or absolute < self.min:
			raise ValueError("Value: " + str(absolute) + " is not valid for this motor. (Max: " + str(self.max) + " Min: " + str(self.min) + ")")
		return absolute

	def percentageToAbsolute(self, percentage):
		if percentage > 1 or percentage < -1:
			raise ValueError("Value: " + str(percentage) + " is not a valid percentage for this motor")
		absolute = self.home
		if percentage > 0:
			absolute += (self.max - self.home) * percentage
		else:
			absolute += (self.home - self.min) * percentage
		return absolute

class Limb:
	def __init__(self, type, side):
		self.type = type
		self.side = side
		self.parts = {}
		if type == Limbs.Leg:
			for legPart in LegParts:
				port = config.getint('motors', side.value + legPart.value + "port")
				home = config.getint('motors', side.value + legPart.value + "home")
				min = config.getint('motors', side.value + legPart.value + "min")
				max = config.getint('motors', side.value + legPart.value + "max")
				self.parts[legPart] = Motor(port, Motors.HS5765, home, min, max)
		else:
			for armPart in ArmParts:
				port = config.getint('motors', side.value + armPart.value + "port")
				home = config.getint('motors', side.value + armPart.value + "home")
				min = config.getint('motors', side.value + armPart.value + "min")
				max = config.getint('motors', side.value + armPart.value + "max")
				self.parts[armPart] = Motor(port, Motors.HS5765, home, min, max)


class MotorStructure:
	def __init__(self):
		self.limbs = {}
		for limb in Limbs:
			newSide = {}
			for side in Side:
				newSide[side] = Limb(limb, side)
			self.limbs[limb] = newSide

class George:

	def __init__(self):
		self.port = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
		self.hash = str(unichr(35))
		self.limbs = {"Arm":["ShoulderUD", "ShoulderLR", "Elbow", "Wrist", "Gripper"]}

	def moveRaw(self, limbs, positions, speeds):
		if speeds == None:
			speeds = [1000 for limb in limbs]
		sendString = ""
		for counter in range(0 ,len(limbs)):
			sendString += self.hash + str(limbs[counter]) + " P" + str(positions[counter]) + " S" + str(speeds[counter])
		self.port.write(sendString + " \r")

	def moveDegrees(self, limbs, positions, speeds=None):
		pins = [config.getint('motors', limb) for limb in limbs]
		stepValues = []
		counter = 0
		for pin in pins:
			if pin < 16:
				if speeds == None:
					speeds = [config.getfloat('motors', 'A_StepperSpeed') for limb in limbs]
				stepPerDegree = config.getfloat('motors', 'A_StepPerDegree')
				stepValues.append(config.getint('motors', limbs[counter] + '_H') + positions[counter] * stepPerDegree)
			counter = counter + 1
	
		self.moveRaw(pins, stepValues, speeds)

	def moveArms(self, w=None,h=None, rotation = None, speed = None):
		forearm = config.getfloat('construction', "forearm_length")
		bicep = config.getfloat('construction', "bicep_length")
		
		term1 = (w ** 2 + h ** 2 + forearm ** 2 - bicep ** 2) / (2 * forearm * (h ** 2 + w ** 2) ** 0.5)
		term2 = (h * 1.0) / w
		theta2 = (math.pi - math.asin(term1)) - math.atan(term2)

		term1 = (h - forearm * math.cos(theta2)) / bicep
		theta1 = math.acos(term1)

		theta1 = math.degrees(theta1)
		theta2 = math.degrees(theta2)

		if w < forearm:
			thetaBicep = -theta1
			thetaForearm = theta2 + theta1
		else:
			thetaBicep = theta1
			thetaForearm = theta2 - theta1

		if not speed is None:
			speed = [speed for i in range(0,3)]

		self.moveDegrees(['A_L_ELBOW','A_L_SHOULDERUD','A_L_SHOULDERLR'], [thetaForearm, thetaBicep, rotation], speed)

	def grip(self, arms, ammount, speed=500):
		pins = [config.getint('motors', 'A_' + arm + "_GRIPPER") for arm in arms]
		am = []
		counter = 0
		for arm in arms:
			am.append((config.getint('motors', "a_" + arm + "_gripClosed") - config.getint('motors',"a_" + arm + "_gripOpen")) * ammount[counter] + config.getint('motors', "a_" + arm + "_gripOpen"))
			counter += 1
		self.moveRaw(pins, am, [speed])

	def home(self):
		for limb in self.limbs['Arm']:
			self.moveRaw(config.get('motors', 'A_L_' + limb), config.get('motors', 'A_L_' + limb + '_H'),config.get('motors', 'A_StepperSpeed'))

	def close(self):
		self.port.close()




test = MotorStructure()
print(test.limbs[Limbs.Arm][Side.Left].parts[ArmParts.Elbow])

time.sleep(10000)

test = George()

test.home()
test.moveArms(22,10,0)
test.grip(["l"],[0.5])
time.sleep(3)
test.grip(["l"],[0])
test.moveArms(1,26,0)
time.sleep(1000000)

while True:
	test.grip(["l"],[0])
	time.sleep(3)
	test.grip(["l"],[1])
	time.sleep(3)

time.sleep(100000)
#test.moveArms(13,10)
#while True:
time.sleep(3)
test.moveArms(22,10,0)
time.sleep(1)
test.moveArms(13,10,0)
time.sleep(1)
#for x in range(13,25):
#	test.moveArms(x,10)
#	time.sleep(2)
#time.sleep(3)
#test.moveArms(18,17)
#time.sleep(3)
#test.home()
while False:
	test.moveDegrees(['A_L_ELBOW','A_L_SHOULDERUD'], [45,-45])
	time.sleep(3)
	test.moveDegrees(['A_L_ELBOW','A_L_SHOULDERUD'], [-45,45])
	time.sleep(3)
while False:
	distance = input("Distance: ")
	test.moveRaw(config.get('motors', 'A_L_ELBOW'), distance,500)
