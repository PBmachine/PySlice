###################################################
# Phoebe DeGroot
# PySlice Mesh Importer v1_01: 20-11-22
#  ____   __  __   ____   __     __   ____   ______   
#  == ==  ==  ==  ==  -=  ==     ==  ==  -=  ==   -
#  ==  =  ==_ ==   -==    ==     ==  ==      ==-=
#  ====   _  ===  =   ==  ==     ==  ==   =  ==   _
#  ==      ====    ====   =====  ==   ====   ======  
# 
################################################### 
#  .venv\scripts\activate
# #                    
# Function:
# opens stl binary mesh file and creates mesh with facets
# creates mesh class containing file header, num facets, list of facets, bounding box
# facet class contains normal vector, array of xyz for vertices, bounding box 
#
# To Do:
# !: write code for sorting, transforming?
# maybe: alternative parsing for ascii format
###################################################

#Binary STL format https://docs.fileformat.com/cad/stl/
# 80 byte header
# 4 byte u_int number of facets
# - for all facets:
# 4 byte, 4 byte, 4 byte - i, j, k float for normal
# 4 byte, 4 byte, 4 byte - x, y, z float for vertex 1
# 4 byte, 4 byte, 4 byte - x, y, z float for vertex 2
# 4 byte, 4 byte, 4 byte - x, y, z float for vertex 3
# 2 byte u_int for attriute byte count (usually null? I think it's unimportant....
# - just ends at the end of the last facet

# may need a handler for determining if file is valid and in what format
# valid binary file should have filesize = num facets *bytes per facet + fileInfo bytes
import struct
import os
import numpy as np

#make a numpy array for facet vertices
#numpy.zeros(shape, dtype=float, order='C', *, like=None)
#https://www.geeksforgeeks.org/data-type-object-dtype-numpy-python/?ref=gcse

##Classes
class Facet(object):
    def __init__(self, normal, v, a):
        #A facet with a normal and three vertices + some other stuff
        self.normal = np.array(normal)
        self.v = np.mat(v)
        self.a = a #attributes - may use to label later
        self.bbox = np.zeros((2,3))
    
    def facetPrint(self):
        print(f'Normal: \t')
        print(self.normal)
        print('Vertices:')
        print(self.v)
        
    def printVertex(self,vertex):
        return(f'x:{vertex[0]}, y:{vertex[1]}, z:{vertex[2]}')


class Mesh(): 
    def __init__(self, fName, fInfo):
        self.fName = fName
        self.header = fInfo[0]
        self.numfacets = fInfo[1]
        self.facets =  [] #should reformat so I can use array
        self.fcoord = np.zeros((self.numfacets,3,3)) #3d array of all facet coordinates 
        self.bbox = np.zeros((2,3))
    
    def getFacets(self):
        #iterates through num facets and makes facets
        for i in range(self.numfacets):
            normal = rVector(self.fName,'float')
            v0 = rVector(self.fName,'float')
            v1 = rVector(self.fName,'float')
            v2 = rVector(self.fName,'float')
            a = struct.unpack('H', self.fName.read(2))[0]
            self.facets.append(Facet(normal, [v0,v1,v2], a))
            self.fcoord[i] = np.asmatrix(self.facets[i].v) 
    
    def printFacetInfo(self,lo=0,hi=-1):
        #prints normals and vertices for all facets in mesh or in selected range
        if hi == -1: hi = self.numfacets
        for i in range(lo,hi):
            print(f'\nFacet {i} -')
            self.facets[i].facetPrint()

    def getBBox(self):
        #base version to find bounding box - fix for efficiency
        #iterate through all vertices and find highest and lowest
        for i in range(self.numfacets):
            facet = self.facets[i]
            maxpts = np.amax(facet.v, axis = 0)
            minpts = np.amin(facet.v, axis = 0)
            facet.bbox = [minpts,maxpts]

        self.bbox[0] = np.amin(self.fcoord,axis = (0,1))
        self.bbox[1] = np.amax(self.fcoord,axis = (0,1))



##>>>>> --------------- Functions ------------------------------------------------------------ <<<<<
#https://docs.python.org/3/library/struct.html struct info
def rFloat(fName):
    bytes8 = fName.read(4)
    return struct.unpack('f', bytes8)[0]

def rVector(fName, vtype):
    #reads a three values from file to form a point or vector 
    #x,y,z or i,j,k
    if vtype == 'float':
        a = rFloat(fName)
        b = rFloat(fName)
        c = rFloat(fName)
    return[a,b,c]

def homog(verts):
    print(f'starting shape:{np.shape(verts)}')
    
    new = np.transpose(verts)
    new = np.append(new,[[1,1,1]], axis = 0)
    print(f'resulting shape:{np.shape(new)}')
    return(new)

#https://docs.python.org/3/library/os.html#miscellaneous-system-information
def checkBinSize(filepath,numfacets):
    facetbytes = 12*4+2
    otherbytes = 80 + 4
    filesize = os.stat(filepath).st_size
    if filesize - otherbytes == numfacets*facetbytes:
        print(f'Created valid Binary File - {numfacets} facets, {filesize} bytes')
        return True
    else:
        print("filesize did not match num facets - check file is in binary STL format")
        return False

def getInfo(myfile):
        header = myfile.read(80)
        numfacets = struct.unpack('I', myfile.read(4))[0]
        return(header,numfacets)
    
##>>>>> --------------- OPEN STL File --------------------------------
def openSTL(filepath):
    mf = open(filepath, 'rb')
    info = getInfo(mf)
    if not(checkBinSize(filepath, info[1])):
        #no handler for ASCII format 
        return 
    myMesh = Mesh(mf,info)
    myMesh.getFacets()
    myMesh.getBBox()
    print('completed parse')
    return myMesh


# filepath = "pysliceMain\Mesh_Models\Cone_10x10_96_bin.stl"
# def importMSH(filepath):

#run()
