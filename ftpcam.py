'''
ftpcam Chimera instrument for automatization of extinction coefficients from allsky images. 
Created by Pedro H. Bernardinelli on Jan 22, 2016.

Allsky function by Germano S. Bortolotto, modified by Pedro. 
Allsky requires the path for the image and star files, the highest magnitude of the stars in the images, filter used in the images (B or R),
sigma deviations from best fit and number of iterations (both to eliminate outliers in the data)

'''

import time
import os
import shutil

from allsky import *


from ftplib import FTP

#Parameters for Allsky:
#Highest values of star magnitudes (between 2 and 3 for best results)
star_mag = 2
#Filter used (B or V)
filter_used = "B"
#Sigma deviations for outliers (between 1.5 and 3)
sigma_dev = 1.5
#Number of iterations (over 10, more if you wish)
niter = 20



def ftpcam():
	ftp = FTP('') #ftp address
	ftp.login('', '') #user and password
	ftp.getwelcome()

	filematch = "*.fits"
	directory = "" #directory of the images on the FTP folder
	ftp.cwd(directory)
	images = "" #local directory for where the images will be analysed by AllSky
	analysed = "" #local directory for where the images will be saved after being analysed
	stars = "" #local directory for the allsky stars files. 
	if not os.path.exists(images):
		os.makedirs(images)
	if not os.path.exists(analysed):
		os.makedirs(analysed)
	if not os.path.exists(stars):
		os.makedirs(stars)

	while True:
		new_images = False

		for filename in ftp.nlst(filematch):
			if os.path.exists(analysed + filename) == False:
				fhandle = open(os.path.join(images, filename), 'wb')
				print 'Copying ' + filename
				ftp.retrbinary('RETR ' + filename, fhandle.write)
				fhandle.close()
				new_images = True

			else:
				print 'File ' + filename  + ' already copied.'
		if new_images:
			Allsky(images, stars, star_mag,filter_used ,sigma_dev, niter)
		new_images = False
		#Allsky requires image_path, star_path, highest value of star magnitudes, filter used in the images (B or R), sigma deviations from best fit
		#and number of iterations to eliminate outliers.
		
		#after Allsky analyses an image, the image is sent to the analysed folder
		for filename in os.listdir(images):
			if filename.endswith(".fits"):
				shutil.move(os.path.join(images,filename), os.path.join(analysed,filename))

		time.sleep(10)
		#wait time for next update on server

ftpcam()