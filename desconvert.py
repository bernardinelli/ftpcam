"""
Created on Jul 13, 2012

@author: Germano S. Bortolotto

desconvert.py --- This program transforms the x, y coordinates from geoxy.py 
into horizontal coordinates (alt,az) for each SASCA image.

Parameters:
    --------
    Use with: $ python altaz2xy.py /path/to/ImagesDirectory/
    
    Where /path/to/ImagesDirectory/ is the path where are the images.
    
Returns:
    --------
    [image].out.xy.done.az
    Table with zenith distance, y, mag V, and name for all the stars.
    
"""

import sys
import glob
import numpy as np

def Desconvert(path):
    print "Starting Desconvert..."

    files_in_a_folder = glob.glob(path + "*.done") 
    
    for file_ in files_in_a_folder:    
        xphoto,y,mags,name = np.loadtxt(file_, unpack=True, usecols=(0,1,2,3))    

        altaz =[]

        col1 = np.array(xphoto)
        col2 = np.array(y)    
        NOV = 1.570796325 #90 degrees in radians
        
        #Convert from cartesian coord to horizontal coords
        #(Actually only the zenith distance -> azimuth is not important here)
        altaz.append([np.sqrt((col1-512)*(col1-512) + (col2-512)*(col2-512))*NOV/512. ,
                      col2, mags, name])
    
        altaz = np.array(altaz)
        altaz = np.column_stack(altaz)
        dataout = np.transpose(altaz)

        #Save the file with zenith distance, y, mag V, name
        coord = open(file_ + '.az', 'w')
        np.savetxt(coord, dataout)

    
if __name__ == "__main__": 
    Desconvert(sys.argv[1])