from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import ncc

##############################################################################
#                            Global "magic numbers"                          #
##############################################################################

# How much to scale each smaller image
scale = 0.75

# Default size for our template image
templateWidth = 15

# Threshold
threshold = 0.5175

# Path to save images
global static
#global image_name


#image_name = "unamed"

def MakePyramid(image, minsize):
	# Initialize the list where we will store the images and place the original image in it.
	pyramid = []
	pyramid.append(image)
	
	# We will check that both the width and height dimensions are largerthan the specified minimum.
	while(image.size[0] > minsize and image.size[1] > minsize):
		# Get the dimensions of the image.
		x = image.size[0]
		y = image.size[1]
		# Make a new copy with scaled dimensions
		image = image.resize((int(x*scale),int(y*scale)),Image.BICUBIC)
		# Append the new image to our list.
		pyramid.append(image)

	return pyramid

def FindTemplate(pyramid, template, threshold):
	# Maintain a variable so we know by how much to scale the coordinates back.
	scaleBack = 1

	matches = []

	# This markerImage will be the image where we draw the rectangles of matches we find.
	markerImage = pyramid[0]
	# Convert it to RGB so we can add coloured rectangles.
	markerImage = markerImage.convert('RGB')

	# Loop over every image in the pyramid to find matches.
	for image in pyramid:
		# Get the normalized cross correlation of the template with the image.
		crossXC = ncc.normxcorr2D(image, template)

		# We loop through this 2D returned array to check for values larger than our threshold.
		for y in range(len(crossXC)):
			for x in range(len(crossXC[y])):
				if crossXC[y][x] > threshold:
					matches.append((x*scaleBack,y*scaleBack,scaleBack))
	
		scaleBack *= 1/scale
	return matches


def DrawFaces(image, matches, template):
	
	width = template.size[0]
	height = template.size[1]

	for i in range(len(matches)):
		s = matches[i][2]
		draw = ImageDraw.Draw(image)
		x1 = matches[i][0] + width/2*s
		x2 = matches[i][0] - width/2*s
		y1 = matches[i][1] + height/2*s
		y2 = matches[i][1] - height/2*s
		
		# Then we use them to draw a green rectangle around the point.
		draw.line((x1,y1,x2,y1),fill="green",width=2)
		draw.line((x1,y2,x2,y2),fill="green",width=2)
		draw.line((x1,y1,x1,y2),fill="green",width=2)
		draw.line((x2,y1,x2,y2),fill="green",width=2)
				
		del draw

	image.show()
	print image_name
	SaveImage(image, "_faces_")
	#image.save()

# param1 = image to save
# param2 = string of type of modification made
def SaveImage(image, type):
	#sub1 = 'static/'
	sub2 = image_name[0:image_name.index('.')]	
	sub3 = type
	sub4 = image_name[image_name.index('.'):len(image_name)]	
	savename = sub2+sub3+sub4
	print savename
	image.save(savename)

def PruneCoordinates(matches, threshold):
	coordinates = []
	checked = []
	for i in range(len(matches)):
		x1 = matches[i][0]
		y1 = matches[i][1]
		count = 0
		for j in range(len(matches)):
			# Make sure we're not looking at the same one
			if i != j and not (j in checked) and not i in checked:
			#if not j in checked:
				x2 = matches[j][0]
				y2 = matches[j][1]

				if math.fabs(x1-x2) < threshold and math.fabs(y1-y2) < threshold:
					count += 1
					checked.append(j)
		
		if count > 0:
			coordinates.append((x1,y1,matches[i][2]))

	return coordinates


# Returns the coordinates of anything found
def GetCoordinates(image_path):	
	#Load image and template. Convert to grey scale (just in case)
	#im = Image.open("testphotos/students.jpg") 
	print image_path
	im = Image.open(image_path) 
	im.convert('L')

	# Keep track of image name so we can use it later
	global image_name
	image_name = image_path.split('/')[-1]
	
	template = Image.open("testphotos/template.jpg")
	# Resize 
	templateHeight = template.size[1]*templateWidth/template.size[0]
	template = template.resize((int(templateWidth),int(templateHeight)),Image.BICUBIC)

	#Create a pyramid of resized images 
	pyramid = MakePyramid(im,templateWidth)

	coordinates = FindTemplate(pyramid, template, threshold)

	coordinates = PruneCoordinates(coordinates, templateWidth/2)
	DrawFaces(im,coordinates,template)

	return coordinates


#GetCoordinates()