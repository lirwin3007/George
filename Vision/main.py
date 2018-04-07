#Import Libaries
from camera import *
from machineLearning import *
import os

#Read in training data
dictionary = {}

for dirPath, dirNames, fileNames in os.walk("Objects"):
	if dirPath != "Objects":
		objectList = []

		for filename in fileNames:
			objectList.append(Image(dirPath + "/" + filename))
		
		dictionary.update({dirPath[8:]:objectList})


#Clear the screen and train the classifier
print("\033[H\033[J")
print("training...")

classifier = create(dictionary, trainNew=True)
myCamera = camera()	#Initialise the camera

counter = 0
filecounter = 0

while True:
	myCamera.update(classifier)	#Update the camera
	myCamera.show()			#Show the camera feed
	counter += 1
	#if counter > 10:
	myCamera.RGB.save("recording/" + str(filecounter) + ".png")
	filecounter += 1
	#	counter = 0
	#	print("photo")

