'''
Modified by Pedro H. Bernardinelli for the ftpcam Chimera instrument. Added fixed inputs for automatization
Jan 22, 2016
'''
"""
Created on Nov 27, 2012

@author: Germano S. Bortolotto
 
subtract.py --- This program subtracts the instrumental magnitude with the zero
point magnitude (MagZero) for each different filter used for all the identified 
stars. This is done separately for each instant in the night and for all the 
instants for a given star.
It also excludes stars up to mag 4 with too few data points or problems in 
localization coordinates.

Parameters:
    --------
    Use with: $ python subtract.py /path/to/ImagesDirectory/ /path/to/StarsDirectory/
    
    Where /path/to/ImagesDirectory/ is the path where are the images, and
    /path/to/StarsDirectory/ is the path where are the individual stars files.
    
Returns:
    --------
    [star name].pdst.tb1
    Table with airmass, instrumental magnitude - MagZero, star name, mag B, 
    mag R, error in instrumental magnitude for all the identified stars 
    throughout the entire night.
    
    [image].pd.t2
    Table with airmass, instrumental magnitude - MagZero, star name, mag B, 
    mag R, error in instrumental magnitude for all the identified stars for a 
    given instant.
    
"""
import sys
import glob
import numpy as np

def CatMag(image_path,star_path, filt):
    print "Starting CatalogMag..."
    
    #Aglutinating files
    DirEstrelas = glob.glob(star_path + "*.pdst")
    DirTempos = glob.glob(image_path + "*.pd")
    
    limAX = 2.5
    #filter = raw_input("Which filter is being used in the images? (B/R): ")
    
    #Zero point magnitudes of the photometric system
    ZeroB = 17.580624041
    ZeroR = 17.709511786
    
    for file1 in DirEstrelas:
        am, mag_inst, B, R, name1, mag_err = np.genfromtxt(file1, unpack=True, 
                                                    usecols = (0,1,2,3,4,5),
                                                    missing_values ='INDEF')
        if filt == 'B':
            menosmag = mag_inst - B - ZeroB 
        if filt == 'R':
            menosmag = mag_inst - R - ZeroR
        else:
            print "Please choose the filter red (R) or blue (B)."
        
        mask1 = np.where((am < limAX) & (name1 != 1852.) & (name1 != 1903.) & 
        (name1 != 1948.) & (name1 != 3165.) & (name1 != 3485.) & (name1 != 3685.) &
        (name1 != 7001.) & (name1 != 4662.) & (name1 != 5958.) & (name1 != 4819.) & 
        (name1 != 5571.) & (name1 != 1788.) & (name1 != 1910.) & (name1 != 3447.) & 
        (name1 != 3940.) & (name1 != 4037.) & (name1 != 4140.) & (name1 != 4844.) & 
        (name1 != 5190. )& (name1 != 5235.) & (name1 != 6410.) & (name1 != 6247.))

        table = np.column_stack([am[mask1], menosmag[mask1], name1[mask1],
                                  B[mask1], R[mask1], mag_err[mask1]])
        if table.size !=0 : 
            result = open(file1 + ".tb1", 'w')
            np.savetxt(result, table, '%s')
    
    
    for file2 in DirTempos: #aqui mag_fev e a mag_zero calculada para cada estrela da noite 08
                            #esta na posicao onde era anteriormente a 'color'
        mag_err2, name2, am2, mag_inst2, B2, R2  = np.genfromtxt(file2, unpack=True, 
                                                        usecols = (0,1,2,3,4,5),
                                                        missing_values =('INDEF', 'nan'))
        if filt == 'B':
            menosmag2 = mag_inst2 - B2 - ZeroB
            #erro = np.sqrt(mag_err2**2 + )
        if filt == 'R':
            menosmag2 = mag_inst2 - R2 - ZeroR
        else:
            print "Please choose the filter red (R) or blue (B)."
            
        mask2 = np.where((am2 < limAX) & (name2 != 1852.) & (name2 != 1903.) &
        (name2 != 1948.) & (name2 != 3165.) & (name2 != 3485.) & (name2 != 3685.) &
        (name2 != 7001.) & (name2 != 4662.) & (name2 != 5958.) & (name2 != 4819.) & 
        (name2 != 5571.) & (name2 != 1788.) & (name2 != 1910.) & (name2 != 3447.) & 
        (name2 != 3940.) & (name2 != 4037.) & (name2 != 4140.) & (name2 != 4844.) &
        (name2 != 5190.) & (name2 != 5235.) & (name2 != 6410.) & (name2 != 6247.))

        #Saves a file with airmass, mag, star_name
        table2 = np.column_stack([am2[mask2], menosmag2[mask2], name2[mask2],
                                  B2[mask2], R2[mask2], mag_err2[mask2]])
                                  
        results2 = open(file2 + ".t2", 'w')
        np.savetxt(results2, table2, '%s')
    
if __name__ == "__main__": 
    CatMag(sys.argv[1],sys.argv[2]) 