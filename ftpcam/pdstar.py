'''
Created on Sep 5, 2012

@author: Germano S. Bortolotto
'''

class StarList:
    """
    This class open the various columns of the file refered to as
    'obj_name' and selects the correct values corresponding to a certain star name. 
    """
        
    def __init__(self, obj_name): #obj_name
  
        import numpy as np
        
        self.name_list = np.loadtxt(obj_name, usecols=[1])
        self.B_list = np.loadtxt(obj_name, usecols=[4])
        self.R_list = np.loadtxt(obj_name, usecols =[5])
        self.mag_list_calc  = np.loadtxt(obj_name, usecols=[3],dtype='string')
        self.mag_list_error  = np.loadtxt(obj_name,usecols=[0],dtype='string')
        self.air_list  = np.loadtxt(obj_name, usecols=[2])
    
    def get_airmass(self, name):
        """
        Return the airmass of an object with name "name"
        """
        from numpy import where
        return self.air_list[where(self.name_list == name)]
    
    def get_B(self, name):
        """
        Return the B outside the atmosphere magnitude of an object with name "name"
        """
        from numpy import where
        return self.B_list[where(self.name_list == name)]
        
    def get_R(self, name):
        """
        Return the R outside the atmosphere magnitude of an object with name "name"
        """
        from numpy import where
        return self.R_list[where(self.name_list == name)]
    
    def get_mag_calc(self, name):
        """
        Return the instruemntal magnitude of an object with name "name"
        """
        from numpy import where
        return self.mag_list_calc[where(self.name_list == name)]
        
    def get_mag_error(self, name):
        """
        Return the instrumental magnitude error of an object with name "name"
        """
        from numpy import where
        return self.mag_list_error[where(self.name_list == name)]
        
    def get_name(self, name):
        """
        Return the name of an object with name "name"
        """
        from numpy import where
        return self.name_list[where(self.name_list == name)]
