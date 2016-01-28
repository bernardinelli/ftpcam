"""
Created on Jul 3, 2012

@author: Germano S. Bortolotto

geoxy.py --- This program distorts the alt, az coordinates from skycalc.py 
into pixel coordinates (X,Y) for each SASCA image.


Parameters:
    --------
    Use with: $ python geoxy.py /path/to/ImagesDirectory/
    
    Where /path/to/ImagesDirectory/ is the path where are the images.
    
Returns:
    --------
    Table with the distorted X,Y coordinates for all the stars 
    
"""

import os
import sys
import glob
from pyraf import iraf


#Getting access to Iraf
login = "home$login.cl"
iraf.task(login = "home$login.cl")
p = iraf.login.getCode()
eval('p')


def Geoxy(path):
    print "Starting Geoxy..."
    filename = path
    os.chdir(filename)   
    corrected = glob.glob("*.xy")
                   
    #Removing existing files    
    filelist = glob.glob("*.done")
    for f in filelist:
        os.remove(f)
    
    #Transforming coordinates
    print "Saving files with the new coordinates."
    for i in corrected:
        iraf.images(_doprint=0)
        iraf.immatch(_doprint=0)
        iraf.geoxy(input=i, output=i+'.done', database='data3', transforms='trans3')     

if __name__ == "__main__": 
    Geoxy(sys.argv[1]) 