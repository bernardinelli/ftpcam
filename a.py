import numpy as np
from astropy.io import fits
import os
import pylab as pl
pl.matplotlib.rc('text', usetex=True)

from run import run

ZP_RED = 17.709511786
ZP_BLUE = 17.580624041

def load_image(file):
	im = fits.open(file)
	return im.data[0]


def dist(im1, im2):
	im = np.mat(im1)*np.mat(im2)
	return np.linalg.norm(im)/(np.linalg.norm(im1)*np.linalg.norm(im2))

def find_max(or_image, group_folder):
	images = []
	files = []
	for i in os.listdir(group_folder):
		if i.endswith(".fits"):
			image = fits.open(group_folder + '/'+ i)
			images.append(image[0].data)
			files.append(i)
			
	or_data = fits.open(or_image)[0].data
	delta = []
	for i in images:
		delta.append(dist(or_data,i))

	maxd, maxp = np.max(delta), np.argmax(delta)

	return np.average(delta), np.max(delta), group_folder + '/' + files[maxp]

images = []
for i in os.listdir('/home/pedro/allsky/GROUP1'):
	if i.endswith(".fits"):
		image = fits.open('/home/pedro/allsky/GROUP1/' + i)
		images.append(image[0].data)
		
x = images[0]
delta = []
for i in images:
	if dist(x,i) > 0.5:
		delta.append(dist(x,i))

pl.hist(delta,20, histtype='step', normed=True)

images = []
for i in os.listdir('/home/pedro/allsky/GROUP2'):
	if i.endswith(".fits"):
		image = fits.open('/home/pedro/allsky/GROUP2/' + i)
		images.append(image[0].data)
delta =[]
for i in images:
	delta.append(dist(x,i))

pl.hist(delta,20, histtype='step', normed=True)

pl.xlabel(r"$\cos\theta$",fontsize=15)
pl.title(r"Histograma de $\cos\theta$ para dois grupos de imagens",fontsize=15)
		
pl.show()


#find_max(x, '/home/pedro/allsky/GROUP1')

def find_group_max(file_n, group1, group2, ZP, mag_cut):
	av_1, max_1, file_1 = find_max(file_n, group1)
	av_2, max_2, file_2 = find_max(file_n, group2)

	coeff_image = run(file_n, mag_cut, ZP)
	print coeff_image
	coeff_1 = run(file_1, mag_cut, ZP)
	print coeff_1
	coeff_2 = run(file_2, mag_cut, ZP)
	print coeff_2

	if max_1 - av_1 >= max_2 - av_2:
		return coeff_1 - coeff_image, 1
	else:
		return coeff_2 - coeff_image, 2

 
print find_group_max('test/lots/cp_b20050726ut232929s71310.fits', '/home/pedro/allsky/GROUP1', '/home/pedro/allsky/GROUP2', ZP_BLUE, 3)


	