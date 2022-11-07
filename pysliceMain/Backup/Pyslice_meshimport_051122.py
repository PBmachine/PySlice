###################################################
# Phoebe DeGroot
#  ____   __  __   ____   __     __   ____   ______   
#  == ==  ==  ==  ==  -=  ==     ==  ==  -=  ==   -
#  ==  =  ==_ ==   -==    ==     ==  ==      ==-=
#  ====   _  ===  =   ==  ==     ==  ==   =  ==   _
#  ==      ====    ====   =====  ==   ====   ======  
# 
###################################################                     
# PySlice Mesh Importer v1_00: 051122
#
# opens stl binary mesh file and creates mesh with facets
# creates mesh class containing file header, num facets, list of facets, bounding box
# facet class contains normal vector, (x,y,z) coord for each vertex, bounding box 
#
# To Do:
# !!: use numpy arrays
# !: write code for sorting, transforming?
# maybe: alternative parsing for ascii format
###################################################

#Binary STL format https://www.loc.gov/preservation/digital/formats/fdd/fdd000505.shtml
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
#https://stackoverflow.com/questions/26171521/verifying-that-an-stl-file-is-ascii-or-binary
import struct
import os

class Facet(object):
    def __init__(self, normal, v0, v1, v2, a):
        #A facet with a normal and three vertices + some other stuff
        self.normal = normal
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.a = a #attributes - may use to label later
        self.min = []
        self.max= []
    
    def facetPrint(self):
        print(f'\t Normal:: i:{self.normal[0]}, j:{self.normal[1]}, k:{self.normal[2]}')
        print(f'\t V0:: {self.printVertex(self.v0)}')
        print(f'\t V1:: {self.printVertex(self.v1)}')
        print(f'\t V2:: {self.printVertex(self.v2)}')
        
    def printVertex(self,vertex):
        return(f'x:{vertex[0]}, y:{vertex[1]}, z:{vertex[2]}')

class Mesh(object): 
    def __init__(self, fName):
        self.fName = fName
        self.header = b'\x00'
        self.numfacets = 0
        self.facets = []
        self.bbox = [[],[]]

    def getInfo(self):
        self.header = self.fName.read(80)
        self.numfacets = struct.unpack('I', self.fName.read(4))[0]
    
    def getFacets(self):
        #iterates through num facets and makes facets
        for i in range(self.numfacets):
            normal = rVector(self.fName,'float')
            v0 = rVector(self.fName,'float')
            v1 = rVector(self.fName,'float')
            v2 = rVector(self.fName,'float')
            a = struct.unpack('H', self.fName.read(2))[0]
            self.facets.append(Facet(normal, v0, v1, v2, a))
    
    def printFacetInfo(self,lo=0,hi=-1):
        #prints normals and vertices for all facets in mesh or in selected range
        if hi == -1: hi = self.numfacets
        for i in range(lo,hi):
            print(f'Facet {i}:')
            self.facets[i].facetPrint()

    def getBBox(self):
        #base version to find bounding box - fix for efficiency
        #iterate through all vertices and find highest and lowest
        for i in range(self.numfacets):
            facet = self.facets[i]
            maxpts = [[],[],[]]
            minpts = [[],[],[]]
            pts = ([],[],[])
            for n in range(3):
                pts[n].append(facet.v0[n])
                pts[n].append(facet.v1[n])
                pts[n].append(facet.v2[n])
            for n in range(3):
                maxpts[n] = max(pts[n])
                minpts[n] = min(pts[n])
            facet.min = minpts
            facet.max = maxpts
            if len(self.bbox[0])==0:
                self.bbox[0]=minpts
                self.bbox[1]=maxpts
            else: 
                for n in range(3):
                    self.bbox[0][n]=min(self.bbox[0][n],minpts[n])
                    self.bbox[1][n]=max(self.bbox[1][n],maxpts[n])


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

#https://docs.python.org/3/library/os.html#miscellaneous-system-information
def checkBinSize(filepath,numfacets):
    facetbytes = 12*4+2
    otherbytes = 80 + 4
    filesize = os.stat(filepath).st_size
    if filesize - otherbytes == numfacets*facetbytes:
        print(f'Valid Binary File - {numfacets} facets, {filesize} bytes')
        return True
    else:
        print("filesize did not match num facets - check file is in binary STL format")
        return False

    
# OPEN STL File
def openSTL(filepath):
    mf = open(filepath, 'rb')  
    myMesh = Mesh(mf)
    myMesh.getInfo()
    if not(checkBinSize(filepath, myMesh.numfacets)):
        #no handler for ASCII format 
        return
    myMesh.getFacets()
    myMesh.getBBox()
    return myMesh


#filepath = "Mesh_Models/Cone_10x10_96_bin.stl"
#openSTL(filepath)
