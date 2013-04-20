from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
from scipy import ndimage
import scipy.misc
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
cat_path = "testphotos/hipcat.png"
catWidth = 90

def GetImagePath(filename):
	image_path = file_path+filename
	image_path = image_path.replace('\\','/')
	return image_path

def LoadImage(filename):
	print "LoadImage"
	image_path = GetImagePath(filename)
	image = Image.open(image_path)
	cat = Image.open(cat_path)

	#Resize Cat
	catHeight = cat.size[1]*catWidth/cat.size[0]
	cat = cat.resize((int(catWidth),int(catHeight)),Image.BICUBIC)

	coordinates = tmatch.GetCoordinates(image_path)
	CopyOver(image, cat, coordinates)

def GaussFilter(filename):
	path = GetImagePath(filename)
	image = Image.open(path)
	gauss_denoised = ndimage.gaussian_filter(image,3)
	image = Image.fromarray(gauss_denoised)
	image.show()

def SharpFilter(filename):
	path = GetImagePath(filename)
	image = Image.open(path)
	
	blurr = ndimage.gaussian_filter(image,5)
	filter_blurr = ndimage.gaussian_filter(blurr,1)
	alpha = 30
	sharpened = filter_blurr + alpha * (blurr - filter_blurr)

	image = Image.fromarray(sharpened)
	image.show()

def CopyOver(image,cat,coordinates):

	#image_array = np.asarray(image)
	#cat_array = np.asarray(cat)

	image_array = np.array(image)
	cat_array = np.array(cat)

	#xBound = image.size[0]
	#yBound = image.size[1]
	xBound = image_array.shape[0]
	yBound = image_array.shape[1]
	#image_array.flags.writeable = True

	for q in range(len(coordinates)):
		#x = int(round(coordinates[q][0] - cat.size[0]*coordinates[q][2],0))
		#y = int(round(coordinates[q][1] - cat.size[1]*coordinates[q][2],0))

		x = int(round(coordinates[q][0]))
		y = int(round(coordinates[q][1]))

		#x = coordinates[q][0]
		#y = coordinates[q][1]

		print coordinates[q]
		print (x,y,coordinates[q][2])
		print ("BOUNDS:",xBound,yBound)
		#if coordinates[q][2] == 1:

		print image.size
		print cat.size

		s = coordinates[q][2]
		
		draw = ImageDraw.Draw(image)

		#image = image.convert('RGBA')
		#cat = cat.convert('RGBA')
		print "MODES"
		print image.mode
		print cat.mode


		cwidth,cheight = cat.size
		cWhalf = cwidth/2
		chhalf = cheight/2
		if x+cwidth < xBound and y+cheight < yBound:
			image.paste(cat, (x-cWhalf,y-chhalf,cwidth+x-cWhalf,cheight+y-chhalf),cat)
			#image.paste(cat, cat.getbbox(), cat)
		
		del draw


	newImage = Image.fromarray(image_array)
	# Uncomment to debug
	#newImage.show()
	#image.show()
	tmatch.SaveImage(image,"_cats_")

"""
coordinates = tmatch.GetCoordinates(image_path)

CopyOver(image, cat, coordinates)
"""
#GaussFilter('students.jpg')
#SharpFilter('students.jpg')
#LoadImage('students.jpg')