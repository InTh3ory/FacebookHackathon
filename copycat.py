from PIL import Image, ImageDraw
import numpy as np
import math
from scipy import signal
from scipy import ndimage
import ImageFilter
import scipy.misc
import tmatch
import os
import random
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

#cat_path = "testphotos/restoration.png"
cats = []
cats.append("testphotos/grumpycat.png")
cats.append("testphotos/hipcat.png")
cats.append("testphotos/restoration.png")
#cat_path = "testphotos/grumpycat.png"
catWidth = 90

def GetImagePath(filename):
	image_path = file_path+filename
	image_path = image_path.replace('\\','/')
	return image_path

def LoadImage(filename):
	print "LoadImage"
	image_path = GetImagePath(filename)
	image = Image.open(image_path)

	cat_path = getRandomCat()

	cat = Image.open(cat_path)

	#Resize Cat
	catHeight = cat.size[1]*catWidth/cat.size[0]
	cat = cat.resize((int(catWidth),int(catHeight)),Image.BICUBIC)

	coordinates = tmatch.GetCoordinates(image_path)
	CopyOver(image, cat, coordinates)

def getRandomCat():
	index = random.randint(0,2)
	return cats[index]


def GaussFilter(filename):
	path = GetImagePath(filename)
	image = Image.open(path)
	image = image.filter(ImageFilter.BLUR)
	save = tmatch.GetSavePathFromName(filename, '_blur_')
	image.save(save);

def SharpFilter(filename):
	path = GetImagePath(filename)
	image = Image.open(path)
	image = image.filter(ImageFilter.SHARPEN)
	save = tmatch.GetSavePathFromName(filename, '_sharp_')
	image.save(save);

def EmbossFilter(filename):
	path = GetImagePath(filename)
	image = Image.open(path)

	image = image.filter(ImageFilter.EMBOSS)

	save = tmatch.GetSavePathFromName(filename, '_emboss_')
	image.save(save);


"""
	Sepia filter based off of Mike Griffith's blog:
	http://www.mike-griffith.com/blog/2010/01/batch-convert-images-to-sepia-tone-with-python/
"""
def SepiaFilter(filename):
	path = GetImagePath(filename)
	image = Image.open(path)

	sepia = make_linear_ramp((255,240,192))

	orig_mode = image.mode
	if orig_mode != 'L':
		image = image.convert('L')

	print image.mode

	image.putpalette(sepia)
	print image.mode
	if orig_mode != 'L"':
		image = image.convert(orig_mode)

	print image.mode

	save = tmatch.GetSavePathFromName(filename, '_sepia_')
	image.show()
	try:
		image.save(save);
	except IOError as e:
			print e
			print "trying to strip alpha channel"
			image = image.convert('L')
			image.save(save)

def make_linear_ramp(colour):
	ramp = []
	r,g,b = colour
	for i in range(255):
		ramp.extend((r*i/255, g*i/255, b*i/255))
	return ramp

def CopyOver(image,cat,coordinates):

	#image_array = np.asarray(image)
	#cat_array = np.asarray(cat)

	cat_path = getRandomCat()
	cat = Image.open(cat_path)

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

		cat_path = getRandomCat()
		cat = Image.open(cat_path)

		#Resize Cat
		catHeight = cat.size[1]*catWidth/cat.size[0]
		cat = cat.resize((int(catWidth),int(catHeight)),Image.BICUBIC) 

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

		cwidth,cheight = cat.size
		cWhalf = cwidth/2
		chhalf = cheight/2
		if x+cwidth < xBound and y+cheight < yBound:
			image.paste(cat, (x-cWhalf,y-chhalf,cwidth+x-cWhalf,cheight+y-chhalf),cat)
		
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


#SepiaFilter('judybats.jpg')

#EmbossFilter('students.jpg')
#GaussFilter('students.jpg')
#SharpFilter('students.jpg')
#LoadImage('students.jpg')