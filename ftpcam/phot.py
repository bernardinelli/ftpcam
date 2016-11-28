'''
Created on Jul 21, 2012

@author: Germano S. Bortolotto

'''

import os
import sys
import glob
from pyraf import iraf

""" 
phot.py --- This program performs photometry for the previously identified stars
using the coordinates obtained via geoxy.py. 

Parameters:
    --------
    Use with: $ python phot.py
    
Returns:
    --------
    Two different tables:
        [image].mag - follows IRAF standards.
        [image].magnitude - A simple list with magnitude, and error of magnitude for
        all stars identified in the field for each image.
"""

#Get access to Iraf
login = "home$login.cl"
iraf.task(login = "home$login.cl")
p = iraf.login.getCode()

eval('p')


def Photometry(path):
    print "Starting Photometry..."
    print "This can take a long time. Go drink some coffee!"
    filename = path #raw_input("Path to the directory of the images: ") 
    os.chdir(filename)   
    
    iraf.noao(_doprint=0)
    iraf.digiphot(_doprint=0)
    iraf.apphot(_doprint=0)

    #Parameter settings
    iraf.centerpars.setParam('calgorithm', 'centroid', check=0, exact=0)
    iraf.centerpars.setParam('cbox', '10.0', check=0, exact=0) 
    iraf.centerpars.saveParList(filename="center.par") 
    iraf.centerpars.setParList(ParList="center.par")

    iraf.fitskypars.setParam('salgorithm', 'mode', check=0, exact=0)
    iraf.fitskypars.setParam('annulus', '7.0') 
    iraf.fitskypars.setParam('dannulus', '2.0', check=0, exact=0)
    iraf.fitskypars.saveParList(filename='fits.par')
    iraf.fitskypars.setParList(ParList='fits.par')

    iraf.photpars.setParam('apertures', '4.5', check=0, exact=0) 
    iraf.photpars.saveParList(filename='phot.par')
    iraf.photpars.setParList(ParList='phot.par')

    iraf.datapars.setParam('fwhm', 'INDEF', check=0, exact=0)
    iraf.datapars.setParam('sigma', 'INDEF', check=0, exact=0)
    iraf.datapars.setParam('datamin', 'INDEF', check=0, exact=0)
    iraf.datapars.setParam('datamax','INDEF', check=0, exact=0)
    iraf.datapars.setParam('ccdread','RESPONSE', check=0, exact=0)
    iraf.datapars.setParam('gain','EGAIN', check=0, exact=0)
    iraf.datapars.setParam('exposur','EXPTIME', check=0, exact=0)
    iraf.datapars.setParam('airmass','AIRMASS', check=0, exact=0)
    #iraf.datapars.setParam('xairmas','1.', check=0, exact=0)
    iraf.datapars.setParam('obstime','UTSHUT', check=0, exact=0)
    iraf.datapars.setParam('filter','FILTER', check=0, exact=0)
    iraf.datapars.saveParList(filename='data.par')
    iraf.datapars.setParList(ParList='data.par')

    #Takes the necessary parameters
    iraf.centerpars.getParam('calgorithm', native=1, mode="h", exact=0, prompt=0)
    iraf.centerpars.getParam('cbox', native=1, exact=0, prompt=0)
    
    iraf.fitskypars.getParam('salgorithm', native=1, mode="h", exact=0, prompt=0)
    iraf.fitskypars.getParam('annulus', native=1, exact=0, prompt=0)
    iraf.fitskypars.getParam('dannulus', native=1, exact=0, prompt=0)

    iraf.photpars.getParam('apertures', native=1, mode="h", exact=0, prompt=0)

    iraf.datapars.getParam('fwhm', native=0, mode='h', exact=0, prompt=0)
    iraf.datapars.getParam('sigma', native=0, mode="h", exact=0, prompt=0)
    iraf.datapars.getParam('datamin', native=0, mode="h", exact=0, prompt=0)
    iraf.datapars.getParam('datamax', native=0, mode="h", exact=0, prompt=0)
    iraf.datapars.getParam('ccdread', native=0, mode="h", exact=0, prompt=0)
    iraf.datapars.getParam('gain', native=0, mode="h", exact=0, prompt=0)
    iraf.datapars.getParam('exposur', native=0, mode="h", exact=0, prompt=0)
    iraf.datapars.getParam('airmass', native=0, mode="h", exact=0, prompt=0)
    iraf.datapars.getParam('xairmas', native=0, mode="h", exact=0, prompt=0)
    iraf.datapars.getParam('obstime', native=0, mode="h", exact=0, prompt=0)
    iraf.datapars.getParam('filter', native=0, mode="h", exact=0, prompt=0)
                
    
    #Removing existing files
    filelist1 = glob.glob("*.mag")
    filelist2 = glob.glob("*.magnitude")

    for f in filelist1:
        os.remove(f)
    for g in filelist2:
        os.remove(g)
        
    #Photometry
    print "Extracting magnitude and magnitude error from the files created by Pyraf"
    images = glob.glob("*.fits")
    for i in images:
        tr_coord = i + '.out.xy.done'
        iraf.phot(image = i, output = i + '.mag', coords = tr_coord, interactive = 'no' , wcsin = 'tv', skyfile = '', verify='no', verbose='no' )


    #uses IRAF's pdump to take MAG values from the PHOT's output file
    photometry = glob.glob("*.mag")                  
    for j in photometry:
        iraf.pdump(j, 'MAG, MERR', 'yes', Stdout = j + 'nitude')
                       
        
if __name__ == "__main__": 
    Photometry(sys.argv[1]) 
