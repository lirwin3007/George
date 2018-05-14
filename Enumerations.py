from enum import Enum

class Motors(Enum):
	"""Motor types, defined by serial number"""
	#:Smaller servo motor
	HS422 = 'HS422'
	#:Larger servo motor
	HS5765 = 'HS5765'

class Side(Enum):
	"""Sides of the body"""
	Left = 'L'
	Right = 'R'

class Limbs(Enum):
	"""Limb types"""
	Arm = 'A'
	Leg = 'L'

class ArmParts(Enum):
	"""Joints of the arm"""
	#:Arm motor moving the shoulder fornt and back
	ShoulderFrontBack = 'SFB'
	#:Motor moving the shoulder left and right
	ShoulderLeftRight = 'SLR'
	#:Elbow joint
	Elbow = 'E'
	#Wrist joint
	Wrist = 'W'
	#:Gripper motor
	Gripper = 'G'

class LegParts(Enum):
	"""Joints of the legs"""
	HipFrontBack = 'HFB'
	HipLeftRight = 'HLR'
	Knee = 'K'
	Foot = 'F'
	
class MovementTypes(Enum):
	"""Types of position"""
	#:Lowest level of control. Provided number directly controls the position of the motor
	Absolute = 0
	#:Provided number represents an angle beween 0 and 360 degrees that the motor will be moved to
	Angle = 1
	#:Number will be be a decimal between 0 and 1 that represents how far the motor must be moved between the minimum and maximum position
	Percentage = 2

class ArmStructure(Enum):
	"""Parts of the structure of the arm"""
	Forearm = 'forearm'
	Bicep = 'bicep'
	Hand = 'hand'

class LegStructure(Enum):
	"""Parts of the structure of the les"""
	Thigh = 'thigh'
	Shin = 'shin'
	Foot = 'foot'

class Positions(Enum):
	"""Poses that can be used"""
	Sitting = 'sitting'
	Standing = 'standing'
