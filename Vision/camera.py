#Import libraries
from SimpleCV import Kinect, DrawingLayer, Display

#Class to represent a camera object
class camera():

    #Subroutine to initialise a new instance of the class
    def __init__(self, internalScaling = 0.5):
        self.kinect = Kinect()  #Variable to hold the kinect object
        self.internalScaling = internalScaling  #Variable to hold the ammount images are scaled by in this class
        self.objects = []   #Array to contain all the object detected in the image

    #Subroutine to update the state of the object
    def update(self, classifier = None):
        self.RGB = self.kinect.getImage()   #Read the image
        self.depth = self.kinect.getDepth() #Read the depth image
	originalSize = self.RGB.size()  #Store the original size - used for scaling

        #Determine the new width and height of the scaled image
	#And then scale the image to correct for camera offset
	newWidth = int(round(originalSize[0]*1.11)) 
	newHeight = int(round(originalSize[1]*1.09))
	self.RGB = self.RGB.scale(newWidth, newHeight)

        #Crop the image and then translate it to further correct for camera offset
	self.RGB = self.RGB.crop(14,75,originalSize[0], originalSize[1])
	self.depth = self.depth.crop(0, 0, self.RGB.size()[0], self.RGB.size()[1])

        #Scale the RGB and depth image by the internal scale factor
        self.scaledRGB = self.RGB.scale(self.internalScaling)
        self.scaledDepth = self.depth.scale(self.internalScaling)

        #Binarise the depth image
        self.binary = self.scaledDepth.binarize(thresh=150)

        #Detect objects in the image
        self.detectObjects(classifier)


    #Subroutine to detect objects in the current camera image
    def detectObjects(self, classifier):
        
        array = self.binary.getNumpy()  #Get the array with the RGB values for the image
	self.objects = []   #Reset the object array

        #Find the pixels grouped together in the binarised depth image
	features = self.binary.findBlobs(minsize=(self.binary.width*self.binary.height)*0.01)

	#If the features array isn't empty
	if features != None:
	        for blob in features:   #Itterate through each grouping of pixels

                    #Store the location and size of the object and use it to crop the image
                    location = (blob.topLeftCorner()[0] / self.internalScaling, blob.topLeftCorner()[1] / self.internalScaling)
                    size = (blob.width()/ self.internalScaling, blob.height() / self.internalScaling)
		    image = self.RGB.crop(location[0],location[1],size[0],size[1])
                    
                    #Append this object to the object array
                    self.objects.append(object(location=location, image=image, size=size, classifier=classifier))


    #Subroutine to show the camera stream with any object that have been detected highlighted
    #Arguments:
    #           Binary - Show the image binarised if True
    #           highlightPixels - Highlights the pixels in the highlightPixels array
    def show(self, binary=False):

        if not binary:
            for object in self.objects:
                object.draw(self.RGB)   #Draw each object
            self.RGB.show() #Show the image
        else:
            largeBinary = self.binary.scale(1/self.internalScaling)
            for object in self.objects:
                object.draw(largeBinary)    #Draw each object
            largeBinary.show()  #Show the image

#Class to represent an object in the image
class object():

    #Subroutine to initialise the class
    def __init__(self, image=None, location = (0,0), size = (0,0), classifier = None):
        
        self.image = image                      #Variable to hold the image of the object
        self.location = location                #Variable to hold the location of the object
        self.size = size                        #Variable to hold the size of the object
        self.colour = (255,0,0)			#Variable to hold the colour of the box drawn around the object

	if classifier != None:
		self.classification = classifier.classify(self.image)
	else:
		self.classification = "Unclassified Object"

            
    #Subroutine to draw the object on a target image
    def draw(self, target):
        layer = DrawingLayer(target.size())     #Create a drawing layer
        #Determine the centerpoint and define a box with this point and size
        centerPoint = (self.size[0] / 2 + self.location[0], self.size[1] /2 + self.location[1])
        box = layer.centeredRectangle(centerPoint, self.size, color = self.colour)
        
        target.addDrawingLayer(layer)   #Add the drawing layer to the target
        #Draw the objects name under the box around it
        target.drawText(self.classification, x= self.location[0], y=self.location[1] + self.size[1], color = self.colour, fontsize=32)

