from pyraf import iraf


login = "home$login.cl"
iraf.task(login = "home$login.cl")
p = iraf.login.getCode()


def geoxy(image):
	iraf.images(_doprint=0)
	iraf.immatch(_doprint=0)
	iraf.geoxy(input=image[:-5] + '.dist', output=image[:-5]+'.done', database='data3', transforms='trans3')   


