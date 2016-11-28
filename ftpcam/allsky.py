'''
Modified by Pedro H. Bernardinelli for the ftpcam Chimera instrument. Added fixed inputs for automatization
Jan 22, 2016
'''
"""
Created on Jul 6, 2012

@author: Germano S. Bortolotto
 
allsky.py --- This is the central program of the AllSky project. It's function
is to call all other programs and execute them one by one.


Parameters:
    --------
    Use with: $ python allsky.py
    The user will be prompted with some questions for the proper behavior of the 
    various programs.
    
    The programs can be used separately.
    For that it is needed to provide in the command line the path to images directory
    and, if needed, the path to the individual stars directory.
    Please refer to the small programs' help docs for more information on how to run
    each script.
    
    A guide with step-by-step usage of allsky.py can be found in the file TUTORIAL.txt.
    
Returns:
    Multiple tables and plots.
    Within the Images directory will be created the following files for each image:
        [image].out - from skycalc.py
        [image].out.xy - from altaz2xy.py
        [image].out.xy.done - from geoxy.py
        [image].out.xy.done.az - from desconvert.py
        [image].out.xy.done.az.am - from airmass.py
        [image].mag - from phot.py
        [image].magnitude - from phot.py
        [image].pd - from instant.py
        [image].pd.t2 - from subtract.py
        [image].pd.t2.png - from linear.py
        
    Within the Individual Stars directory will be created the following files for
    each identified star:
        [star].pdst - from starlist.py
        [star].pdst.tb1 - from subtract.py
        [star].pdst.tb1.png - from linear.py
        
    Please refer to each indicated program for detailed information.
    
"""

import airmass
import altaz2xy
import desconvert
import geoxy
import instant
import linear
import phot
import skycalc
import starlist
import subtract
import sys

def Allsky(image_path, star_path, mag_cut, filt, sigma, Niter):
    
    #Defining the paths
    #image_path = raw_input("Path to the directory of the images: ")
    #star_path = raw_input("Path to the directory individual star files: ")
    
    skycalc.Calc(image_path, mag_cut) 
    altaz2xy.Convert(image_path)
    geoxy.Geoxy(image_path)
    phot.Photometry(image_path)
    desconvert.Desconvert(image_path)
    airmass.Airmass(image_path)
    instant.ImageTable(image_path)
    starlist.StarTable(image_path, star_path)
    subtract.CatMag(image_path, star_path, filt)

    #Calculating the atmospheric extinction coefficient
    linear.Fitting(image_path, star_path, sigma, Niter)

if __name__ == "__main__": 
    Allsky(sys.argv[1:]) 
