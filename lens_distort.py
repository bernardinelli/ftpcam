import numpy as np 
import pylab as pl
import pyfits as pf
import ephem
import re
import fileinput

#Coisa bem copiada do Allsky do Germano
def n_lens_distort(alt, azi, params=[0.,0.,0.,512.]):
	#params = azimuth zero point, x and y offsets
	halfpi = np.pi/2.

	x = (halfpi-alt)*(params[3]/halfpi)*np.cos(azi + halfpi + params[0]) + params[3] + params[1]
	y = (halfpi-alt)*(params[3]/halfpi)*(-1.)*np.sin(azi+halfpi + params[0]) + params[3] + params[2]

	return y, x

'''
#Coisa copiada do PyASB
def lens_distortion(x, y, azimuth, radial_factor):
	Calculates the distortion from an horizontal 
		image to a fish-eye image, 
		using an equal-area zenithal projection
	r_theta = np.sqrt(x**2 + y**2.)/radial_factor

	if r_theta > 360./np.pi:
		r_theta = 360./np.pi

	altitute_factor = 1 - 0.5*(np.pi*r_theta/180.)**2.

	theta = 180./np.pi*np.arcsin(altitute_factor)
	phi = (360+azimuth+180.*np.arctan2(y,-x)/np.pi)%360

	return theta,phi
'''


'''
The following is adapted from Germano's skycalc code. The code was copied and then edited for the purposes of this application.
In his code, he follows a file path and calculates the sky for all images there. Here, we will use a single fits image.
'''

def skycalculator(image, mag_cut):
	file = pf.open(image)
	header, data = file[0].header, file[0].data

	observation = ephem.Observer()
	observation.lat  = '-30:10:20.86692'
	observation.long = '-70:48:00.15364'
	observation.elevation = 2123.090
	observation.date = ephem.date(re.sub('-','/',header['date'])+' '+header['utshut'])

	bright_star_catalog ='BSC.edb'
	star_pos = []

	for line in fileinput.input(bright_star_catalog):  
		star = ephem.readdb(line)
		star.compute(observation)
		if (float(star.mag) < mag_cut):
			line = line.split(',')
			line[6].rstrip()
			star_pos.append([float(star.alt) , float(star.az), float(star.mag), float(star.name), float(line[6])])      
		star_position = open(image[:-5] + '.stars', 'w')
		np.savetxt(star_position, star_pos, '%s')
		star_position.close()



def save_data(image):
	alt, az,  mag, name1, name2 = np.loadtxt(image[:-5] + '.stars', unpack=True)

	x = []
	y = []

	for i in range(len(alt)):
		a,b = n_lens_distort(az[i], alt[i])
		x.append(a)
		y.append(b)

	zipped = zip(x,y,mag,name1,name2)

	np.savetxt(image[:-5] + '.dist', zipped, fmt="%f")

