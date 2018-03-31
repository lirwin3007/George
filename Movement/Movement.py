import serial
import time
import ConfigParser
import math

config = ConfigParser.RawConfigParser()
config.read('config.cfg')

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
