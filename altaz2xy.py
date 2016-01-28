"""
Created on May 21, 2012

@author: Germano S. Bortolotto
 
altaz2xy.py --- This program transforms the alt, az coordinates from skycalc.py 
into pixel coordinates (X,Y) for each SASCA image.

Parameters:
    --------
    Use with: $ python altaz2xy.py /path/to/ImagesDirectory/
    
    Where /path/to/ImagesDirectory/ is the path where are the images.
    
Returns:
    --------
    [image].out.xy
    Table with X,Y coordinates, mag V, name and color index (B-V) for all the stars 
    
"""

import glob
import numpy as np

def Convert(path):
    print "Starting altaz2xy..."
    hor_coord = glob.glob(path + "*.out")       
    
    for i in hor_coord:    
        alt, az, mags, name, bv = np.loadtxt(i, unpack=True, usecols = (0,1,2,3,4)) 
        
        xy =[]
    
        NOVENTA = 1.570796325 #90 degrees in radians
        
        #Coordinate transformations 
        mask = np.where(alt >= 0 )
        alt = alt[mask]
        az = az[mask]
        mags = mags[mask]
        name = name[mask]
        bv = bv[mask]

        xy.append([(NOVENTA-alt)*(512./NOVENTA)*np.cos(az+NOVENTA)+512. ,
                   (NOVENTA-alt)*(512./NOVENTA)*(-1)*np.sin(az+NOVENTA)+512., 
                    mags, name, bv])
        
        xy = np.column_stack(xy)
        dataout = np.transpose(xy)
        coord = open(i + '.xy', 'w')
        np.savetxt(coord, dataout, '%s')
        coord.close()
    
if __name__ == "__main__": 
    Convert(sys.argv[1]) 