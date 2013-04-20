from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
import tmatch
import os
"""
image_path = "testphotos/students.jpg"


catWidth = 60


image = Image.open(image_path) 
cat = Image.open(cat_path)

#Resize Cat
catHeight = cat.size[1]*catWidth/cat.size[0]
cat = cat.resize((int(catWidth),int(catHeight)),Image.BICUBIC)
"""
file_path = os.getcwd() + "\\static\\"
cat_path = "testphotos/blackcat.png"
catWidth = 60

def LoadImage(filename):
	print "LoadImage"
	image_path = file_path+filename
	image_path = image_path.replace('\\','/')
	image = Image.open(image_path)
	cat = Image.open(cat_path)

	#Resize Cat
	catHeight = cat.size[1]*catWidth/cat.size[0]
	cat = cat.resize((int(catWidth),int(catHeight)),Image.BICUBIC)

	coordinates = tmatch.GetCoordinates(image_path)
	CopyOver(image, cat, coordinates)

def CopyOver(image,cat,coordinates):

	image_array = np.asarray(image)
	cat_array = np.asarray(cat)

	xBound = image.size[0]
	yBound = image.size[1]

	image_array.flags.writeable = True

	print (cat_array[1][1][0])

	for q in range(len(coordinates)):
		#x = int(round(coordinates[q][0] - cat.size[0]*coordinates[q][2],0))
		#y = int(round(coordinates[q][1] - cat.size[1]*coordinates[q][2],0))

		x = coordinates[q][0]
		y = coordinates[q][1]

		#for i in range(cat.size[0]):
		for i in range(cat_array.shape[0]):
			#for j in range(cat.size[1]):
			for j in range(cat_array.shape[1]):
				if (x >= 0 and y >= 0) and (x+i < xBound and y+j < yBound) :
					#print cat_array[i][j]
					#print image_array[i][j]
					#image_array[x+i][y+j] = cat_array[i][j][0]
					try:
						image_array[x+i][y+j] = cat_array[i][j][0]
					except IndexError as e:
						print e
						print cat_array[i][j]
						pass

	newImage = Image.fromarray(image_array)
	# Uncomment to debug
	#newImage.show()
	tmatch.SaveImage(newImage,"_cats_")

"""
coordinates = tmatch.GetCoordinates(image_path)

CopyOver(image, cat, coordinates)
"""