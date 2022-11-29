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
# Function:
# opens stl binary mesh file and creates mesh with facets
# creates mesh class containing file header, num facets,
#   dict of facets stored by key (zmin,zmax), list of keys, bounding box
# facet class contains normal vector, array of xyz for vertices, bounding box 
# function for homogenizing coordinated - row or column major
# 
# Next steps: 
# review data sort and store method
# ascii file handler
###################################################
import struct
import os
import numpy as np

##>>>>> --------------- Classes ------------------------------------------------------------ <<<<<
class Facet(object):
    def __init__(self, normal, v, a):
        #A facet with a normal and three vertices + 
        self.normal = np.array(normal)
        self.v = np.mat(v)
        self.a = a #attributes - unused in standard STL format
        self.bbox = np.zeros((2,3))
    
    def facetPrint(self):
        print(f'Normal: \t')
        print(self.normal)
        print('Vertices:')
        print(self.v)

    def getbBox(self):
        maxpts = np.amax(self.v, axis = 0)
        minpts = np.amin(self.v, axis = 0)
        self.bbox[0] = minpts
        self.bbox[1] = maxpts
        print(f' bounding box', self.bbox)
        return self.bbox
        
    def printVertex(self,vertex):
        return(f'x:{vertex[0]}, y:{vertex[1]}, z:{vertex[2]}')


class Mesh(): 
    def __init__(self, fName, fInfo):
        self.fName = fName
        self.header = fInfo[0]
        self.numfacets = fInfo[1]
        self.fcoord = np.zeros((self.numfacets,3,3)) #3d array of all facet coordinates 
        self.bbox = np.zeros((2,3))
        self.dfacets = dict() #all mesh facets stored by key = (zmin,zmax)
        self.lookup = [] #sorted list of facet keys 
    
    def getFacets(self):
        #iterates through num facets and makes facets
        for i in range(self.numfacets):
            normal = rVector(self.fName,'floatR')
            v0 = rVector(self.fName,'floatR')
            v1 = rVector(self.fName,'floatR')
            v2 = rVector(self.fName,'floatR')
            a = struct.unpack('H', self.fName.read(2))[0]

            #create facet and store in dict and matrix
            facet = Facet(normal, [v0,v1,v2], a)
            self.addToFacetDict(facet)
            self.fcoord[i] = np.asmatrix([v0,v1,v2]) 

    def addToFacetDict(self,facet):
        #create facet label as zmin,zmax and store in dict
        #for non-z slicing need generalization or temporarily rotate model to z plane   
        facet.getbBox()
        l = tuple((facet.bbox[0,2], facet.bbox[1,2]))

        if l in self.dfacets: 
            self.dfacets[l] += [facet]
        else:
            self.dfacets[l]=[facet]

    def facetkeyList(self):
        #creates sorted lookup list by zmin values
        self.lookup = sorted(self.dfacets.keys())
        return self.lookup

    def printFacetInfo(self,lo=0,hi=-1):
        #prints normals and vertices for all facets in mesh or in selected range
        if hi == -1: hi = self.numfacets
        for i in range(lo,hi):
            print(f'\nFacet {i} -')
            f = self.nFacet(i)
            f.facetPrint
    
    def nFacet(self,n):
        #returns the nth facet of the mesh
        i = 0
        while i <= n:
            if i == n:
                return self.dfacets[self.lookup[i]][0]
            else: 
                l = len(self.lookup[i])
                if i+l>n:
                    return self.nFacet(n-i)
                i += l

    def getBBox(self):
        #find max and min pts
        self.bbox[0] = np.amin(self.fcoord,axis = (0,1))
        self.bbox[1] = np.amax(self.fcoord,axis = (0,1))
        return self.bbox



##>>>>> --------------- Functions ------------------------------------------------------------ <<<<<

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
    elif vtype == 'floatR': #4 dec round to aide future calculations 
        a = round(rFloat(fName), 4)
        b = round(rFloat(fName), 4)
        c = round(rFloat(fName), 4)
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
    myMesh.facetkeyList()
    myMesh.getBBox()
    print('completed parse')
    return myMesh

##>>>>> --------------- Additional ------------------------------------------------------------ <<<<<

def testcone():
    #test function to check code
    filepath = "Mesh_Models\\Cone_10x10_96_bin.stl"
    myMesh = openSTL(filepath)
    myMesh.printFacetInfo(0,1)
    print(f'\nMesh Bounding Box: {myMesh.bbox}')
    F0 = myMesh.nFacet(0).v
    print(f'homogenized coordinate\n {homog(F0)}')

#Binary STL format https://docs.fileformat.com/cad/stl/
# 80 byte header
# 4 byte u_int number of facets
# - for all facets:
# 4 byte, 4 byte, 4 byte - i, j, k float for normal
# 4 byte, 4 byte, 4 byte - x, y, z float for vertex 1
# 4 byte, 4 byte, 4 byte - x, y, z float for vertex 2
# 4 byte, 4 byte, 4 byte - x, y, z float for vertex 3
# 2 byte u_int for attriute byte count (usually null? I think it's unimportant...

# valid binary file should have filesize = num facets *bytes per facet + fileInfo bytes

#numpy matrices
#https://www.geeksforgeeks.org/data-type-object-dtype-numpy-python/?ref=gcse
