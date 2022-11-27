###################################################
# Phoebe DeGroot
# PySlice Slicer
#  ____   __  __   ____   __     __   ____   ______   
#  == ==  ==  ==  ==  -=  ==     ==  ==  -=  ==   -
#  ==  =  ==_ ==   -==    ==     ==  ==      ==-=
#  ====   _  ===  =   ==  ==     ==  ==   =  ==   _
#  ==      ====    ====   =====  ==   ====   ======  
#         
###################################################                   
# Function:
# create polygonal slice from 
# To Do:
# !: write code for sorting, transforming?
# maybe: alternative parsing for ascii format
###################################################

import numpy as np



class slice(object):
    def __init__(self,seq):
        self.seq = seq
        self.points = np.array()
        self.ocontour = []
        self.icontour= []

class infill(object):
    pass

        

class subMesh(object):
    def __init__():
        pass





#slicing
#find intersecting facets
#calculate intersections and convert to segments
#join segments - sort inner and outer contours
#create slices 