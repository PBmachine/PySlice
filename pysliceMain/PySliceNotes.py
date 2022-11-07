#################################################
#  ____   __  __   ____   __     __   ____   ______   
#  == ==  ==  ==  ==  -=  ==     ==  ==  -=  ==   -
#  ==  =  ==_ ==   -==    ==     ==  ==      ==-=
#  ====   _  ===  =   ==  ==     ==  ==   =  ==   _
#  ==      ====    ====   =====  ==   ====   ======  
#                           
#Demo 1: use of parametric primitive rather than vertices 
# Vase style printing (single layer, no infill)
# maybe also 
#
#################################################
"""
class for each slice - polygons outer side



input for layer height
input for nozzle width
input for radial overlap 
input for max overhang

recursion
take current layer 
use vertices to find the next polygon
"""

"""
1. import mesh:
-get triangles to numpy arrays?
-get basic info for mesh (top, bottom, numfaces,bounding box?)
-> reorient etc from user

2. get parameters
- slice height
-tolerance
uh
(nozzle size, offset, dynamic vs static height etc)
yeah

3. start slicing
start the slice
iterate through triangles getting topmost and bottom most points to get list of facets
get rid of facets that are all below we wont need them anymore
compute intersection at height for each facet into a vector
link vectors for that slice
classify interior vectors and multi poylgons
move to next slice until done

4. maybe go and check layers and do stuff

5. Render slices
"""
#>>>-----Generate Slices-----<<<<
class Slice(object):
    def __init__(self, num):
        #num for ordering
        self.num = num
        #((x,y,z),pttype) pttype = print transfer
        self.points = []
        
        
