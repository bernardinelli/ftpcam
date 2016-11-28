import numpy as np
import pylab as pl 

def organize(image, zero_point):
	file = image[:-5]

	true_mag = np.loadtxt(file + '.stars', usecols=[2])

	posx, posy, a, b, c = np.loadtxt(image[:-5] + '.dist', unpack=True)

	inst_mag, sig_mag = np.genfromtxt(file + '.magnitude', unpack = True)

	mag_true = []
	mag_obse = []
	mag_errr = []
	x = []
	y = [] 


	for i in range(len(true_mag)):
		if ~np.isnan(inst_mag[i]):
			mag_true.append(true_mag[i])
			mag_obse.append(inst_mag[i] - zero_point)
			mag_errr.append(sig_mag[i])
			x.append(posx[i])
			y.append(posy[i])

	return mag_true, mag_obse, mag_errr, x, y

def organize2(image, zero_point):
	file = image[:-5]

	true_mag = np.loadtxt(file + '.stars', usecols=[2])

	inst_mag, sig_mag = np.genfromtxt(file + '.magnitude2', unpack = True)

	posx, posy, a, b, c = np.loadtxt(image[:-5] + '.done', unpack=True)

	mag_true = []
	mag_obse = []
	mag_errr = []
	x = []
	y = []


	for i in range(len(true_mag)):
		if ~np.isnan(inst_mag[i]):
			mag_true.append(true_mag[i])
			mag_obse.append(inst_mag[i] - zero_point)
			mag_errr.append(sig_mag[i])
			x.append(posx[i])
			y.append(posy[i])

	return mag_true, mag_obse, mag_errr, x, y


def plot(image, zero_point):
	mag_t, mag_o, mag_s, x, y = organize(image, zero_point)
	a,b = np.polyfit(mag_t, mag_o, 1, w=1./np.asarray(mag_s))
	pl.plot(np.unique(mag_t), np.poly1d(a,b)(np.unique(mag_t)))
	pl.errorbar(mag_t, mag_o, yerr=mag_s, fmt='.')
	'''

	for i in range(len(mag_t)):
		s = "(" + str(int(x[i])) + ", " + str(int(y[i])) + ")"
		pl.annotate(s, xy=(mag_t[i],mag_o[i]), fontsize=7)
		
	'''

	pl.xlabel(r"$m_\mathrm{true}$")
	pl.ylabel(r"$m_\mathrm{obs}$")

	pl.savefig(image[:-5]+'.pdf')

	pl.close('all')

def plot2(image, zero_point):
	mag_t, mag_o, mag_s, x, y = organize2(image, zero_point)
	a,b = np.polyfit(mag_t, mag_o, 1, w=1./np.asarray(mag_s))
	pl.plot(np.unique(mag_t), np.poly1d(a,b)(np.unique(mag_t)))
	pl.errorbar(mag_t, mag_o, yerr=mag_s, fmt='.')


	pl.xlabel(r"$m_\mathrm{true}$")
	pl.ylabel(r"$m_\mathrm{obs}$")
	'''
	for i in range(len(mag_t)):
		s = "(" + str(int(x[i])) + ", " + str(int(y[i])) + ")"
		pl.annotate(s, xy=(mag_t[i],mag_o[i]), fontsize=7)
		
	'''

	pl.savefig(image[:-5]+'_2.pdf')

	pl.close('all')

