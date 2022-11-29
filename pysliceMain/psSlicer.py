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

#almostEqual from 15-112 code
def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)


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


def slicebyZ(mesh, h):
    mesh.checksort() 
    zmax = mesh.bbox()[1,2]
    #offset invoked to avoid slice-vertex intersection
    zh = mesh.bbox()[0,2]+mesh.offset 
    sliceAt(mesh,zh)
    zh = round(zh,4) + h 
    count = 1 
    while zh < zmax:
        sliceAt(mesh,zh)
        zh += h
        count += 1
    print(f'slicing complete: created {count} slices')


def sliceAt(mesh,zh):
    #check facet group

    #iterate through facets in group 
    # if fzmin<zh< fzmax calculate intersection
    # add to slice lines

    # if at end create contour and return

    pass

def intersection(facet, zh):
    #calculating the intersection of triangle facet and z aligned plane
    #for Z slicing 
    ZN = np.array([0,0,1])
    ZP = np.array([0,0,zh])
    #facet pts
    p = []
    for i in range(3):
        p.append(facet.v[i].reshape((3,),order='C'))
    #facet edges
    V=np.zeros((3,3))
    V[0] = p[1]-p[0]
    V[1] = p[2]-p[1]
    V[2] = p[0]-p[2]

    #S intersection params
    S = []
    for i in range(3):
        st = np.dot(ZN,(ZP-p[i]))/np.dot(ZN,V[i])
        S.append(st)

    I = []
    #intersection defined by two points
    for i in range(3):
        #exclude the point where S is out of range
        if (S[i]>=0) and (S[i]<=1):
            I.append(p[i]+S[i]*V[i])
    # print(I[0],I[1])
    return (I)



class slice(object):
    def __init__(self,z):
        self.z = z
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


def test():
    filepath = "Mesh_Models\\box_12_bin.stl"
    testMesh = msh.openSTL(filepath)
    F1 = testMesh.nFacet(1)
    line1 = intersection(F1,1.5)

test()

#slicing
#find intersecting facets
#calculate intersections and convert to segments
#join segments - sort inner and outer contours
#create slices 