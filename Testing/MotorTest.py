import sys
sys.path.append('/home/pi/George/Movement')
sys.path.append("..")

from Enumerations import *
from Movement import *
import time

def main():
	body = MotorStructure()
	body.initMotors()
	time.sleep(2)

	for side in Side:
		for part in LegParts:
			motor = body.limbs[Limbs.Leg][side].parts[part]
			straightMovement = MotorMovement([motor],[0])
			upMovement = MotorMovement([motor],[20])
			downMovement = MotorMovement([motor],[-20])

			straightMovement.execute(body.port)
			time.sleep(2)
			upMovement.execute(body.port)
			time.sleep(2)
			downMovement.execute(body.port)
			time.sleep(2)

if __name__ == "__main__":
	main()
