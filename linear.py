'''
Modified by Pedro H. Bernardinelli for the ftpcam Chimera instrument. Added fixed inputs for automatization and appends to results to a file and
output files for the chi^2 fit and airmass estimation.
Jan 22, 2016
'''
"""
Created on Nov 14,2013

@author: Germano S. Bortolotto

linear.py --- This program calculates the extinction coeffcient by two 
different methods:
    
    The first one calculates the extinction coefficient based on the information
    obtained by the observation of a star throughout the entire night. This 
    information is found in the file ending in .tb1.
    
    The second method calculates the extinction coefficient for every instant
    of the night. The information of airmass and variation in magnitude for all
    the identified stars in each image is found in the file ending in .t2.

Using a derivation of the sigma_clipping algorithm from Astropy, sasca_linalg.py
excludes the data points which deviates more than a certain number of sigma defined
by the user.

The new set of data points is used in a linear least-squares fit to obtain the
extinction coefficient.

For the star files, the program obtains the total, first-order and second order
(color dependant) extinction coefficient.

Both results (for the individual stars and for each instant in the night) are 
saved in plots with airmass X magnitude. The value of the extinction coefficient
can be seen on each plot.
    
Parameters:
    --------
    Use with: $ python linear.py /path/to/ImagesDirectory/ /path/to/StarsDirectory/
    
    Where /path/to/ImagesDirectory/ is the path where are the images, and
    /path/to/StarsDirectory/ is the path where are the individual stars files.
    
Returns:
    --------
    [star name].pdst.tb1.png
    A plot of Observed magnitude X Airmass of the refered star. The linear 
    least-squares fit is shown, as well as the outliers and errorbars. The value
    of the total,first order and second order extinction coefficients are indicated.
    
    [image].pd.t2.png
    A plot of (Observed magnitude - magnitude outside the atmosphere) X Airmass
    of the refered star. The linear least-squares fit is shown, as well as the 
    outliers and errorbars. The value of the total extinction coefficient is 
    indicated.
    
"""

import sys
import glob
import numpy as np
import matplotlib.pyplot as plt

def sigma_clip1(X, Y, cor, erro, sig, iters=100,
               maout=False):                  
    X = np.array(X, copy=False)
    Y = np.array(Y, copy=False)
    Z = np.array(cor, copy=False)
    A = np.array(erro, copy=False)
    X = X.ravel()
    Y = Y.ravel()
    Z = Z.ravel()
    A = A.ravel()
    maskY = np.ones(Y.size, bool)
    if iters is None:
        i = -1
        lastrej = sum(maskY) + 1
        while(sum(maskY) != lastrej):
            h = np.column_stack([X,Z*X,np.ones(len(X))])
            k1, k2, m0 = np.linalg.lstsq(h,Y)[0]
            i += 1
            n = len(Y[maskY])
            lastrej = sum(maskY)
            novoH = np.column_stack([X[maskY],Z[maskY]*X[maskY],np.ones(len(X[maskY]))])
            do = Y[maskY] - np.dot(novoH, [k1,k2,m0])
            maskY = np.abs(do) <= np.sqrt(sum((do)**2)/n) * sig
        iters = i + 1
    for i in range(iters):
        h = np.column_stack([X,Z*X,np.ones(len(X))])
        k1, k2, m0 = np.linalg.lstsq(h,Y)[0]
        novoH = np.column_stack([X[maskY],Z[maskY]*X[maskY],np.ones(len(X[maskY]))]) 
        do = Y[maskY] - np.dot(novoH, [k1,k2,m0])
        n = len(Y[maskY])
        maskY = np.abs(do) <= np.sqrt(sum((do)**2)/n) * sig
        error = np.sqrt(sum((do)**2)/n) * sig
        return X[maskY], Y[maskY], Z[maskY] , A[maskY], error, n         

def sigma_clip2(X, Y, erro, sig, iters=100,
               maout=False):         
                   
    X = np.array(X, copy=False)
    Y = np.array(Y, copy=False)
    erro = np.array(erro, copy=False)
    X = X.ravel()
    Y = Y.ravel()
    erro = erro.ravel()
    maskY = np.ones(Y.size, bool)

    if iters is None:
        i = -1
        lastrej = sum(maskY) + 1
        while(sum(maskY) != lastrej):
            h = np.column_stack([X,np.ones(len(X))])
            k1, m0 = np.linalg.lstsq(h,Y)[0]
            i += 1
            n = len(Y[maskY])
            lastrej = sum(maskY)
            novoH = np.column_stack([X[maskY],np.ones(len(X[maskY]))])
            do = Y[maskY] - np.dot(novoH, [k1,m0])
            maskY = np.abs(do) <= np.sqrt(sum((do)**2)/n) * sig
        iters = i + 1
    for i in range(iters):
        h = np.column_stack([X,np.ones(len(X))])
        k1, m0 = np.linalg.lstsq(h,Y)[0]
        novoH = np.column_stack([X[maskY],np.ones(len(X[maskY]))]) 
        do = Y[maskY] - np.dot(novoH, [k1,m0])
        n = len(Y[maskY])
                
        maskY = np.abs(do) <= np.sqrt(sum((do)**2)/n) * sig
        #error = np.sqrt(sum((do)**2)/n) * sig
        return X[maskY], Y[maskY], erro[maskY]#, error, n 

def Fitting(image_path, star_path, sigma, Niter):
   
    #Aglutinating files
    DirEstrelas = glob.glob(star_path + "*.tb1")
    DirTempos = glob.glob(image_path + "*.t2")    
    
    #sigma = input("""How many sigma deviations from best fit do you want to consider
    #to eliminate outliers in your data? """)    
    #Niter = input("""How many iterations do you want to perform in your data to
    #eliminate the outliers? """ )    
    
    for file1 in DirEstrelas:
        
        airmass_temp , mag_temp , B, R, err_temp = np.genfromtxt(file1, unpack=True,
                                                                 usecols = (0,1,3,4,5), 
                                                missing_values =('INDEF', 'nan', 'None'))
        name = np.loadtxt(file1, unpack = True, usecols = [2], dtype = 'string') 
        
        mask =  ~ np.isnan(mag_temp)
        airmass = airmass_temp[mask]
        mag = mag_temp[mask]
        B = B[mask]
        R = R[mask]
        err = err_temp[mask]
        mag = mag_temp[mask]
        name = name[mask]
        
        color = B-R
        
        if len(airmass) > 3:
            
            #Based on the sigma clipping algorithm from Astropy
            a, b, c, d, m, n  = sigma_clip1(airmass, mag, color, err, sig=sigma, iters=Niter,
                                        maout=False)
                                        
            #The least-squares linear fit
            h1 = np.column_stack([a,c*a,np.ones(len(a))])
            k1, k2, m0 = np.linalg.lstsq(h1,b)[0]  
            k = k1 + k2*color[0]
            R1 = np.column_stack([airmass,np.ones(len(airmass))])     
            teste1 = np.dot(R1,[k,m0])
            with open("airmass.dat","a") as fil:
                s = "%s %f %f %f\n"%(str(file1), k, k1, k2*color[0])
                fil.write(s)
                fil.close()
            print  file1, k, k1,k2*color[0]

            coef = u"HR %s: k = %3f, k' = %3f, k'' = %3f " %(name[0],k, k1, k2) 

            #Configuring and saving the plot
            plt.clf()
            plt.ylim([-1,2.5])
            plt.xlim([0.98,2.5])
            plt.text(1, 2.3 , coef, fontsize=12)    
            plt.xlabel("$Massa\/de\/ar$", fontsize = "20")
            plt.ylabel(u"$M-M_0$", fontsize = "16")
            fig = plt.gcf()
            fig.set_size_inches(12,8)
            plt.plot(airmass, mag, 'ko', label='data')
            plt.errorbar(a, b, yerr=d, fmt='ro')
            plt.plot( airmass, teste1, '-k')
            #plt.legend(str(mag_cat[0]), title = str(k))
            plt.savefig(file1 +'.png', format='png', bbox_inches='tight')
            
        else:
            print "Not enough values to start least-squares"

    for file2 in DirTempos:
        airmass_temp , mag_temp , B, R, err_temp = np.genfromtxt(file2, unpack=True, usecols = (0,1,3,4,5), missing_values =('INDEF', 'nan', 'None'))
        mask =  ~ np.isnan(err_temp)
        airmass = airmass_temp[mask]
        err = err_temp[mask]
        mag = mag_temp[mask]
        B = B[mask]
        R = R[mask]
        err = err_temp[mask]

        color = B-R
        
        #Based on the sigma clipping algorithm from Astropy
        e, f, h = sigma_clip2(airmass, mag, err, sig=sigma,
                                        iters=Niter, maout=False)
              
        #The least-squares linear fit
        R1 = np.column_stack([airmass,np.ones(len(airmass))])     
        new = np.column_stack([e,np.ones(len(e))])
        kim, m0 = np.linalg.lstsq(new,f)[0]
        with open("least_squares_fit.dat","a") as fil:
            s = "%s %f\n"%(str(file2), kim)
            fil.write(s)
            fil.close()     
        print file2, kim
        
        R2 = np.column_stack([airmass,np.ones(len(airmass))])  
        teste2 = np.dot(R2,[kim,m0])
        coef = u"k = %3f" %kim 

        #Configuring and saving the plot
        plt.clf()
        plt.ylim([0,2.0])
        plt.xlim([1,2.5])
        plt.text(1.2, 1.8 , coef, fontsize=12)    
        plt.xlabel("$Massa\/de\/ar$", fontsize = "20")
        plt.ylabel(u"$M-M_0$", fontsize = "16")
        fig = plt.gcf()
        fig.set_size_inches(12,8)
        plt.plot( airmass,mag, 'ko' )
        plt.errorbar(e, f, yerr=h, fmt='ro')
        plt.plot(airmass, teste2, '-r')
        plt.savefig(file2 +'.png', type = 'png')
        
if __name__ == "__main__": 
    Fitting(sys.argv[1],sys.argv[2]) 