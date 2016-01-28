'''
Modified by Pedro H. Bernardinelli for the ftpcam Chimera instrument. Added fixed inputs for automatization
Jan 22, 2016
'''
"""
Created on May 02, 2012

@author: Germano S. Bortolotto
 
skycalc.py --- This program uses PyEphem (version 3.7.3.4) to compute stellar positions.
The database is provided by the Bright Star Catalog.
The BSG contains star name, spectral type, declination, right ascention, mag V,
epoch and color index (B-V).
Additional information is taken from the images headers with the use of PyEphem 
The alt ,az coordinates are calculated only for stars with V < 3.

Parameters:
    --------
    Use with: $ python skycalc.py /path/to/ImagesDirectory/
    
Returns:
    --------
    [image].out
    Table with (alt,az) coordinates, magnitude and name for all the stars with 
    mag V < 3 for the time and local given in image headers.
"""
import ephem
import glob
import ephem.stars
import numpy as np
import pyfits as pf
import sys
import re
import fileinput

def Calc(path, mag_cut):
    print "Starting Skycalc..."
    #mag_cut = raw_input("Highest value of magnitude of the stars: ")
    print "Calculating star positions. Please wait."  
    #os.chdir("/home/germano/workspace/SkyCalc/ImageFiles")
    images = glob.glob(path + "*.fits")

    for i in images:
        f = pf.open(i)
        h, d = f[0].header, f[0].data

        Obs = ephem.Observer()

        #Obs data    
        Obs.lat = '-30:10:20.86692'
        Obs.long = '-70:48:00.15364'
        Obs.elevation = 2123.090
        Obs.date = ephem.date(re.sub('-','/',h['date'])+' '+h['utshut'])
        star_pos = [] 
        
        #Position calculations
        BSC = path + 'BSC.edb' #Bright Star Catalog

        for line in fileinput.input(BSC):  
            star = ephem.readdb(line)
            star.compute(Obs)
            if (float(star.mag) < mag_cut):
                line = line.split(',')
                line[6].rstrip()
                star_pos.append([float(star.alt) , float(star.az), float(star.mag), float(star.name), float(line[6])])      

        star_position = open(i + '.out', 'w')
        np.savetxt(star_position, star_pos, '%s')
        star_position.close()


if __name__ == "__main__": 
    Calc(sys.argv[1]) 