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


# """
# Slice loop
# define a z cutting plane

# loop - over all facets or facets in range
# find facets that intersect with that plane

# loop-until all facets cycled through
# calculate the intersection contour
# store the intersection contour as vector in the slice

# loop 
# sort line segment vectors to construct layer contour
# label and store as slice

# continue until final z height reached

# """

class slice(object):
    def __init__(self,z):
        self.z = z
        self.segments = []
        self.contour = []

    def printsegment(self):
        for s in self.segments:
            p1 = round(s[0][0],2), round(s[0][1],2)
            p2 = round(s[1][0],2), round(s[1][1],2)
            print(f'{p1}->{p2}')
    

class countour(object):
    def __init__(self):
        
        self.points = []
        self.type = ''

class meshslices(object):
    def __init__(self):
        self.slices = []

    def printslices(self):
        for s in self.slices:
            print(f'Slice: Z: {round(s.z,2)}')
            s.printsegment()

def slicebyZ(mesh, h):
    data = meshslices()
    mesh.checkSort() 
    zmax = mesh.bbox[1,2]
    #offset invoked to avoid slice-vertex intersection
    zh = mesh.bbox[0,2]+mesh.offset 
    data.slices.append(sliceAt(mesh,zh))
    zh = round(zh,4) + h 
    count = 1 
    while zh < zmax:
        data.slices.append(sliceAt(mesh,zh))
        zh += h
        count += 1
    print(f'slicing complete: created {count} slices')
    return data


def sliceAt(mesh,zh):
    #naive search (all facets)
    zslice = slice(zh)
    for n in range(mesh.numfacets):
        facet = mesh.nFacet(n)
        if (facet.bbox[0,2]<zh) and (facet.bbox[1,2]>zh):
            zslice.segments.append(intersection(facet,zh))
    return zslice


    # for f in facets: 
    #     if zmin(f)<zh and zmax(f)>zh:
    #         for facet in mesh.dfacets:
    #             pass
    #         segment = intersection[f]

    #iterate through facets in group 
    # if at end create contour and return


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





def test():
    filepath = "Mesh_Models\\box_12_bin.stl"
    testMesh = msh.openSTL(filepath)
    F1 = testMesh.nFacet(1)
    line1 = intersection(F1,1.5)


#slicing
#find intersecting facets
#calculate intersections and convert to segments
#join segments - sort inner and outer contours
#create slices 