import numpy as np
import pylab as pl
from scipy.stats import sigmaclip
pl.matplotlib.rc('text', usetex=True)



def fit(mag_d, air_m, sig_m):
	clipped = sigmaclip(air_m, 3, 3)[0]
	new_a = []
	new_m = []
	new_s = []
	for i in range(len(air_m)):
		if air_m[i] in clipped:
			new_a.append(air_m[i])
			new_m.append(mag_d[i])
			new_s.append(sig_m[i])

	a,b = np.polyfit(new_m, new_a, 1, w=1./np.asarray(new_s))
	return new_m, a, b



def airmass(az):
	deg = np.rad2deg(az)
	with np.errstate(divide='ignore', invalid='ignore'):
		air = np.true_divide(1., np.cos(az)+0.50572*(96.07995-deg)**(-1.6364))
		if ~np.isfinite(air):
			air = 0
	return air


def calculate_airmass(image,zero_point):
	alt, az,  true_mag, name1, name2 = np.loadtxt(image[:-5] + '.stars', unpack=True)

	inst_mag, sig_mag = np.genfromtxt(image[:-5] + '.magnitude', unpack = True)

	mag_diff = []
	air_mass = []
	mag_errr = []


	for i in range(len(true_mag)):
		if ~np.isnan(inst_mag[i]):
			mag_diff.append(-inst_mag[i]+true_mag[i]+zero_point)
			air_mass.append(airmass(az[i]))
			mag_errr.append(sig_mag[i])

	return mag_diff, air_mass, mag_errr



def calculate_airmass2(image,zero_point):
	alt, az,  true_mag, name1, name2 = np.loadtxt(image[:-5] + '.stars', unpack=True)

	inst_mag, sig_mag = np.genfromtxt(image[:-5] + '.magnitude2', unpack = True)

	mag_diff = []
	air_mass = []
	mag_errr = []


	for i in range(len(true_mag)):
		if ~np.isnan(inst_mag[i]):
			mag_diff.append(-inst_mag[i]+true_mag[i]+zero_point)
			air_mass.append(airmass(az[i]))
			mag_errr.append(sig_mag[i])


	return mag_diff, air_mass, mag_errr



def plot(image, zero_point):

	mag_d, air_m, sig_m = calculate_airmass(image, zero_point)

	pl.errorbar(air_m, mag_d, yerr=sig_m, fmt='.')

	pl.ylabel(r"$m_\mathrm{true} - m_\mathrm{obs}$")
	pl.xlabel(r"$X (\mathrm{airmass})$")

	pl.xlim([0.98,2.5])

	pl.savefig(image[:-5] + '_airmass.pdf')

	pl.close('all')



def plot2(image, zero_point):

	mag_d, air_m, sig_m = calculate_airmass2(image, zero_point)

	new_m, a, b = fit(mag_d, air_m, sig_m)
	
	ax = pl.subplot(111)
	pl.plot(np.unique(new_m), np.poly1d(a,b)(np.unique(new_m)))
	pl.text(0.8,0.05,"$k = $" + format(b,'.3f'),fontsize=13,transform=ax.transAxes)
	pl.errorbar(air_m, mag_d, yerr=sig_m, fmt='.')

	pl.ylabel(r"$m_\mathrm{true} - m_\mathrm{obs}$")
	pl.xlabel(r"$X (\mathrm{airmass})$")

	pl.xlim([0.98,2.5])	

	pl.savefig(image[:-5] + '_airmass2.pdf')

	pl.close('all')

	return a







plot2('cp_r20050726ut000320s73110.fits', 17.709511786)