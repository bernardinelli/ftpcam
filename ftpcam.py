'''
ftpcam Chimera controller for automatization of extinction coefficients from allsky images. 
Created by Pedro H. Bernardinelli on Jan 22, 2016.

Allsky function by Germano S. Bortolotto, modified by Pedro. 
Allsky requires the path for the image and star files, the highest magnitude of the stars in the images, filter used in the images (B or R),
sigma deviations from best fit and number of iterations (both to eliminate outliers in the data)

Two .dat files are created in the process inside the images folder. All the .fits files are moved to the analysed folder,
and all the allsky files are stored in the images and stars folders. 

This version uses the chimera object so it becomes a chimera controller.

'''

import time
import os
import shutil

from chimera.core.chimeraobject import ChimeraObject

from allsky import *


from ftplib import FTP

#Parameters for Allsky:
#Highest values of star magnitudes (between 2 and 3 for best results)
star_mag = 2
#Filter used (B or R)
filter_used = "B"
#Sigma deviations for outliers (between 1.5 and 3)
sigma_dev = 1.5
#Number of iterations (over 10, more if you wish)
niter = 20

class Ftpcam(ChimeraObject):
	ChimeraObject.__init__(self)
	def __init__(self):
		self.ftp = ["","",""] #address, username and password
		self.folder = ["",""] #ftp images folder and local directory where AllSky will perform
		self.params = [2, "B", 1.5, 20] #highest star magnitude, filter used, sigma deviations from best fit and number of iterations to eliminate outliers

	def set_ftp(self, address, user = "", password = ""):
		self.ftp = [address, user, password]

	def set_folder(self, ftp, local):
		self.folder = [ftp, local]

	def set_params(self, mag, imfilter, sigma, iterations):
		self.params = [star_mag, imfilter, sigma, iterations]

	def ftpcam(self):
		ftp = FTP(self.ftp[0]) #ftp address
		ftp.login(self.ftp[1], self.ftp[2]) #user and password
		ftp.getwelcome()

		filematch = "*.fits"
		directory = self.folder[0] #directory of the images on the FTP folder
		ftp.cwd(directory)
		images = self.folder[1] + "images/" #local directory for where the images will be analysed by AllSky
		analysed = self.folder[1] +  "analysed/" #local directory for where the images will be saved after being analysed
		stars = self.folder[1] +  "stars/" #local directory for the allsky stars files. 

		if not os.path.exists(images):
			print "Hey, where is your images folder?"
			return 0
		if not os.path.exists(analysed):
			os.makedirs(analysed)
		if not os.path.exists(stars):
			print "Hey, where is your stars folder?"
			return 0

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
				Allsky(images, stars, self.params[0], self.params[1], self.params[2], self.params[3])
			new_images = False
			#Allsky requires image_path, star_path, highest value of star magnitudes, filter used in the images (B or R), sigma deviations from best fit
			#and number of iterations to eliminate outliers.
			
			#after Allsky analyses an image, the image is sent to the analysed folder
			for filename in os.listdir(images):
				if filename.endswith(".fits"):
					shutil.move(os.path.join(images,filename), os.path.join(analysed,filename))

			time.sleep(10)
			#wait time for next update on server

#ftpcam()

def test():
	a = Ftpcam()
	print "Ftpcam testing script! Let's see if this works."

	#print "Enter all string values between quotation marks so Python doesn't think they are variables or numbers."

	ftp = raw_input("Enter the ftp address:")
	usr = raw_input("User name:")
	pwd = raw_input("Password:")
	a.set_ftp(str(ftp), str(usr), str(pwd))

	folder_1 = raw_input("Enter the path to folder where the images are located in the ftp, ending in /:")
	folder_2 = raw_input("Enter the path to the main ftpcam folder, where the images and stars folders are located, again ending in /:")
	a.set_folder(str(folder_1), str(folder_2))

	mag = input("Enter the highest value of the star magnitudes in the images (from 2 to 3):")
	fil = raw_input("Enter the filter used in the images (B or R)")
	sig = input("Enter the sigma deviations to eliminate outliers (from 1.5 to 3):")
	ite = input("Enter the number of iterations for AllSky (from 10 to 20 for optimal results):")
	a.set_params(float(mag), str(fil), float(sig), int(ite))

	print "Everything is set! Ftpcam will start running (hopefully)"

	a.ftpcam()





