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
import psMeshimport as msh


"""
Slice loop
define a z cutting plane

loop - over all facets or facets in range
find facets that intersect with that plane

loop-until all facets cycled through
calculate the intersection contour
store the intersection contour as vector in the slice

loop 
sort line segment vectors to construct layer contour
label and store as slice

continue until final z height reached

"""
#plane ax+by+cz+d=0 
#normal = V1 x V2 


def slicebyZ(mesh, h, offset = 0.00001):
    z = mesh.bbox()[0,2]
    count = 0
    while zh < (mesh.bbox()[1,2]+offset):
        zh = round(z,4)+offset #ensures non intersection with vertices
        sliceAt(mesh,zh)
        z += h
        count += 1
    print(f'slicing complete: created {count} slices')


def sliceAt(mesh,zh):
    pass



class slice(object):
    def __init__(self,seq):
        self.seq = seq
        self.points = np.array()
        self.contour = []

class countour(object):
    def __init__(self):
        self.points = []
        self.type = ''

class infill(object):
    #infill is not included in this version
    pass
       

class subMesh(object):
    def __init__():
        pass





#slicing
#find intersecting facets
#calculate intersections and convert to segments
#join segments - sort inner and outer contours
#create slices 