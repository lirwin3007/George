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
	def __init__(self, motors, positions, speed = -1, speeds = [],  positionType = MovementTypes.Angle, speedType = MovementTypes.Percentage):
		#validation
		if len(motors) != len(positions) or len(motors) == 0:
			raise Exception("Length of motors != length of positions")	

		#Self variable setting
		self.speeds = []
		if speeds == [] and speed == -1:
			self.speeds = [config.getfloat('motors', motor.type.value + "speed") for motor in motors]
		elif len(speeds) != len(motors) and speed == -1:
			print("WARNING: Number of speeds does not match number of motors. Setting all to default value")
			self.speeds = [config.getfloat('motors', motor.type.value + "speed") for motor in motors]
		elif speeds != []:
			self.speeds = speeds
		elif speed != -1:
			if speedType == MovementTypes.Percentage:
				for motor in motors:
					self.speeds.append(config.getfloat('motors', motor.type.value + "speed") * speed)
			elif speedType == MovementTypes.Absolute:
				self.speeds = [speed for motor in motors]
			else:
				raise Exception("Invalid speed type: " + speedType)
		else:
			print("WARNING: Motor speeds have not been set")

		self.motors = motors
		if positionType == MovementTypes.Absolute:
			self.positions = positions
		elif positionType == MovementTypes.Angle:
			self.positions = []
			for counter in range(0, len(motors)):
				self.positions.append(motors[counter].angleToAbsolute(positions[counter]))
				print(motors[counter])
		elif positionType == MovementTypes.Percentage:
			self.positions = []
			for counter in range(0, len(motors)):
				self.positions.append(motors[counter].percentageToAbsolute(positions[counter]))

	def execute(self, port):
		sendString = ""
		for counter in range(0, len(self.motors)):
			sendString += chr(35) + str(self.motors[counter].port) + " P" + str(self.positions[counter]) + " S" + str(self.speeds[counter])
		sendString += " \r"
		port.write(sendString.encode())


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
				self.parts[legPart] = Motor(port, Motors.HS5765, home, max, min)
		else:
			for armPart in ArmParts:
				port = config.getint('motors', side.value + armPart.value + "port")
				home = config.getint('motors', side.value + armPart.value + "home")
				min = config.getint('motors', side.value + armPart.value + "min")
				max = config.getint('motors', side.value + armPart.value + "max")
				self.parts[armPart] = Motor(port, Motors.HS422, home, max, min)


class MotorStructure:
	def __init__(self):
		self.port = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
		self.limbs = {}
		for limb in Limbs:
			newSide = {}
			for side in Side:
				newSide[side] = Limb(limb, side)
			self.limbs[limb] = newSide

	def moveArms(self, w=None,h=None, rotation = None, speed = 1):
		forearmLength = config.getfloat('construction', ArmStructure.Forearm.value + "length")
		bicepLength = config.getfloat('construction', ArmStructure.Bicep.value + "length")

		term1 = (w ** 2 + h ** 2 + forearmLength ** 2 - bicepLength ** 2) / (2 * forearmLength * (h ** 2 + w ** 2) ** 0.5)
		term2 = (h * 1.0) / w
		theta2 = (math.pi - math.asin(term1)) - math.atan(term2)

		term1 = (h - forearmLength * math.cos(theta2)) / bicepLength
		theta1 = math.acos(term1)

		theta1 = math.degrees(theta1)
		theta2 = math.degrees(theta2)

		if w < forearmLength:
			thetaBicep = -theta1
			thetaForearm = theta2 + theta1
			print("option 1")
		else:
			thetaBicep = theta1
			thetaForearm = theta2 - theta1
			print("option 2")

		motors = [self.limbs[Limbs.Arm][Side.Left].parts[ArmParts.Elbow]]
		motors.append(self.limbs[Limbs.Arm][Side.Left].parts[ArmParts.ShoulderFrontBack])
		motors.append(self.limbs[Limbs.Arm][Side.Left].parts[ArmParts.ShoulderLeftRight])

		print(thetaForearm)
		print(thetaBicep)
		print(rotation)

		armMovement = MotorMovement(motors, [thetaForearm, thetaBicep, rotation], speed=speed)
		armMovement.execute(self.port)



test = MotorStructure()
while True:
	test.moveArms(22,4,0,2)
	time.sleep(1)
	test.moveArms(13,4,0,2)
	time.sleep(3)
