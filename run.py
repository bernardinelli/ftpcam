import lens_distort as l 
import photometry as p
import fix_and_plot as f 
import numpy as np
import geo as g
import airmass as a

ZP_RED = 17.709511786
ZP_BLUE = 17.580624041

def run(image, mag_cut, zero_point):
	l.skycalculator(image,mag_cut)
	l.save_data(image)

	g.geoxy(image)

	p.photometry(image)
	p.photometry2(image)

	f.plot(image, zero_point)
	f.plot2(image,zero_point)

	a.plot(image, zero_point)
	air = a.plot2(image, zero_point)
	return air

'''
files = np.genfromtxt('test/allsky/new.dat',dtype=str)

for i in files:
	run('test/allsky/' + i, 3, ZP_RED)'''

run('cp_r20050726ut002316s74310.fits', 3, ZP_RED)