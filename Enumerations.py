from enum import Enum

class Motors(Enum):
	HS422 = 'HS422'
	HS5765 = 'HS5765'

class Side(Enum):
	Left = 'L'
	Right = 'R'

class Limbs(Enum):
	Arm = 'A'
	Leg = 'L'

class ArmParts(Enum):
	ShoulderFrontBack = 'SFB'
	ShoulderLeftRight = 'SLR'
	Elbow = 'E'
	Wrist = 'W'
	Gripper = 'G'

class LegParts(Enum):
	HipFrontBack = 'HFB'
	HipLeftRight = 'HLR'
	Knee = 'K'
	Foot = 'F'
	
class MovementTypes(Enum):
	Absolute = 0
	Angle = 1
	Percentage = 2
