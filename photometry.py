from pyraf import iraf

#iraf parameters copied from Germano's code
login = "home$login.cl"
iraf.task(login = "home$login.cl")
p = iraf.login.getCode()

eval('p')



def photometry(image):
	#iraf parameters copied from Germano's code

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

    iraf.phot(image = image, output = image[:-5] + '.mag', coords = image[:-5] + '.dist', interactive = 'no' , wcsin = 'tv', skyfile = '', verify='no', verbose='no' )
    iraf.pdump(image[:-5] + '.mag', 'MAG, MERR', 'yes', Stdout = image[:-5] + '.magnitude')

def photometry2(image):
    #iraf parameters copied from Germano's code

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

    iraf.phot(image = image, output = image[:-5] + '.mag', coords = image[:-5] + '.done', interactive = 'no' , wcsin = 'tv', skyfile = '', verify='no', verbose='no' )
    iraf.pdump(image[:-5] + '.mag', 'MAG, MERR', 'yes', Stdout = image[:-5] + '.magnitude2')