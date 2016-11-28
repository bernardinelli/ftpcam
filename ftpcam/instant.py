"""
Created on Feb 20, 2014

@author: Germano S. Bortolotto
 
instant.py --- This program organizes all the information obtained so far of the
stars in each image (airmass, magnitude, error in magnitude, star name) with the
respectives outside the atmosphere magnitudes in filter B and R.

Parameters:
    --------
    Use with: $ python instant.py /path/to/ImagesDirectory/
    
    Where /path/to/ImagesDirectory/ is the path where are the images.
    
Returns:
    --------
    [image].pd
    Table with magnitude error, name, airmass, instrumental magnitude, magB and
    mag R for all the identified stars in the image.
    
"""

import sys
import glob
import numpy as np
import pandas as pd


def ImageTable(image_path):
    
    filename = image_path 

    #File with the calculated MagZero for all the identified stars in filter B and R
    name, B, R = np.loadtxt(image_path + 'MagZero', unpack= True, usecols = (0,1,2) )
     
    files_in_a_folder = glob.glob(filename + "*.fits")
    
    for file_ in files_in_a_folder:
        obj_name  = np.loadtxt(file_ +".out.xy.done", unpack =True, usecols = [3])
        obj_mag = np.loadtxt(file_ + ".magnitude", unpack = True, usecols=(0,1),
                             dtype='string')
        obj_airmass = np.loadtxt(file_ + ".out.xy.done.az.am", usecols=[0])
        
        #Creates data frames from the data provided
        gh = pd.DataFrame({'names' :name, 'magB' : B, 'magR' :R})
        df = pd.DataFrame({ 'names':obj_name, 'obj_mag' : obj_mag[0], 
                           'mag_error': obj_mag[1], 'obj_airmass' : obj_airmass})
        new_df = pd.DataFrame()

        #Selects only the stars with determined mag from outside the atmosphere 
        for i in gh['names']:
            new_df = new_df.append(df.ix[df['names'] == i], ignore_index=True)
        
        data = pd.merge(new_df, gh, on='names')
        data.to_csv(file_ + '.pd', index = False, header = False, sep =' ',
                   float_format='%s')

if __name__ == "__main__": 
    ImageTable(sys.argv[1]) 
