#Import Libaries
import os, shutil
from SimpleCV import *

def create(classes,trainNew=True):
	if not trainNew:
		return TreeClassifier.load('tree.dat')

	#Setup directory structure
	shutil.rmtree("test")
	shutil.rmtree("train")
	os.makedirs("test")
	os.makedirs("train")
	for Class in classes:
		os.makedirs("test/" + Class)
		os.makedirs("train/" + Class)
		counter = 0
		for image in classes[Class]:
			image.save("train/" + Class + "/" + str(counter) + ".png")
			counter += 1

	#Execute trainer code
	executeString = "python trainer.py -c '"
	for Class in classes:
		executeString += Class + ","
	executeString = executeString[:-1]
	executeString += "' -s tree"
	os.system(executeString)

	#Read in result and store
	return TreeClassifier.load('tree.dat')
