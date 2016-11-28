"""
Created on Sep 20, 2012

@author: Germano S. Bortolotto
 
airmass.py --- This program calculates the airmass based on the zenith 
distance calculated by desconvert.py for every previously identified star in each 
SASCA image. The airmass is calculated using the Kasten & Young Formula:
Kasten, F. & Young, A.T. Revised optical air mass tables and approximation 
formula. Applied optics 28, 4735-4738 (1989).


Parameters:
    --------
    Use with: $ python altaz2xy.py /path/to/ImagesDirectory/
    
    Where /path/to/ImagesDirectory/ is the path where are the images.
    
Returns:
    --------
    [image].out.xy.done.az.am
    Table with airmass, mag V, name and hour of the image for all the stars
    in each image from SASCA.
    
"""

import os
import numpy as np
import sys
import glob

def Airmass(image_path):
    print "Starting Airmass..."
    filename = image_path 
    os.chdir(filename) 
    files_in_a_folder = glob.glob("*.az")
    
    for file_ in files_in_a_folder:     

        X = []
        z, coluna, mags, name = np.loadtxt(file_, unpack=True, usecols = (0,1,2,3)) 
        z = np.array(z)
        coluna = np.array(coluna)
        
        #Calculate airmass using the Kasten & Young formula
        cosZrad = np.cos(z)       
        Zdec = np.rad2deg(z)

        X.append([np.divide(1., cosZrad+0.50572*(96.07995-Zdec)**(-1.6364)), 
                  mags, name])

        #Saves a file with airmass, instrumental magnitude and star_name 
        X = np.array(X)
        X = np.column_stack(X)
        dataout = np.transpose(X)
        texto = open(file_ +'.am', 'w')
        np.savetxt(texto, dataout, '%s' , newline='\n')


if __name__ == "__main__": 
    Airmass(sys.argv[1]) 
