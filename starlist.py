"""
Created on Apr 27, 2014

@author: Germano S. Bortolotto

starlist.py --- This program separates the data of the entire night, organized by
instant.py, to each of the stars. 


Parameters:
    --------
    Use with: $ python instant.py /path/to/ImagesDirectory/ /path/to/StarsDirectory/
    
    Where /path/to/ImagesDirectory/ is the path where are the images, and
    /path/to/StarsDirectory/ is the path to put the individual stars files.
    
Returns:
    --------
    [star].pdst
    Table with magnitude error, name, airmass, instrumental magnitude, magB and
    mag R for each [star]. This data covers the information of all the instants
    of the night (all the images).
    
"""
import os
import glob  
import pdstar
import numpy as np
import sys

def StarTable(image_path, star_path):
            
    # Setting Paths            
    name, B, R = np.loadtxt(image_path + 'MagZero', unpack= True, usecols = (0,1,2) )
    files_in_a_folder = glob.glob(image_path + "*.fits")    
    destination_path = star_path     
    
    print "Starting Starlist..."
    
    #Removing existing files    
    filelist = glob.glob(destination_path + "*.pdst")
    for f in filelist:
        os.remove(f)    
    
    for file_ in files_in_a_folder:
    
        obj_name    = file_ + ".pd"
        myStarList = pdstar.StarList(obj_name)
    
        #Data for each star using all the images
        for i in myStarList.get_name(myStarList.name_list):
            lists = []
            lists.append([myStarList.get_airmass(i), 
                          myStarList.get_mag_calc(i),
                          myStarList.get_B(i), 
                          myStarList.get_R(i), 
                          myStarList.get_name(i),
                          myStarList.get_mag_error(i)])
            
            lists = np.column_stack(lists)
            final_list = np.transpose(lists)
            antares = open(destination_path + str(i) + '.pdst', 'a')
    
            np.savetxt(antares, final_list, '%s')
            
if __name__ == "__main__": 
    StarTable(sys.argv[1],sys.argv[2]) 