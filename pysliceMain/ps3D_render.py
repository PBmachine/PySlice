###################################################
# Phoebe DeGroot
# PySlice 3D Viewer
#  ____   __  __   ____   __     __   ____   ______   
#  == ==  ==  ==  ==  -=  ==     ==  ==  -=  ==   -
#  ==  =  ==_ ==   -==    ==     ==  ==      ==-=
#  ====   _  ===  =   ==  ==     ==  ==   =  ==   _
#  ==      ====    ====   =====  ==   ====   ======  
# 
###################################################                     
# Function:
# 
#
# To Do:
# 
###################################################

# """
#put in the base template stuff for animations
# render the lines
#rendering to make further back stuff less bright - could do distance calc or fake it relative to pixel y value - zcoordinate

#http://www.codinglabs.net/article_world_view_projection_matrix.aspx
# 3D object transforms using 4d vectors- we can set this as [0,0,0,1]
#[[Xx,Yx,Zx,Tx],[Xy,Yy,Zy,Ty],[Xz,Yz,Zz,Tz],[0,0,0,1]]
# the x, y and z values change direction and scale of object coordinate system
# for simple translation use identity matrix for x,y,z and tx,ty,tz for the local xyz origin
# for everything else t column should be 0,0,0,1
# simple rotation the axis cell = 1, rest of row, col = 0 and then the relevant sin/cos(angle) for the other two axes



# """

import math
import numpy as np
#https://www.compuphase.com/axometr.htm
def rad(degree):
    return math.radians(degree)

class trans:
    def __init__(self):
        self.theta = 0
        self.shift = np.zeros((3,1))

class iso(object):
    def __init__(self,angle,origin,scale):
        self.a = math.radians(angle)
        self.o = origin
        self.scale = scale
        
        
    def isoXY(self,pt):
        x = pt[0]*self.scale
        y = pt[1]*self.scale
        z = pt[2]*self.scale
        xP = self.o[0]+x*math.cos(self.a)-y*math.cos(self.a)
        yP = self.o[1]- x*math.sin(self.a) - y*math.sin(self.a) - z
        return([xP,yP])



    




def dimXY(v,ox,oy,scale):
    #dimetric projection of xyz coord to x,y coord
    xP = (v[0]*math.cos(rad(7))+(v[1]*math.cos(rad(42)))/2) * scale
    yP = (v[1]+(v[1]*math.sin(rad(42)))/2-v[0]*math.sin(rad(7))) * scale
    xP += ox
    yP += oy
    return [xP,yP]

# OLD
# def isoXY(v,ox,oy,scale):
#     #isometric projection of xyz coord to x,y coord
#     xP = ((v[0]-v[2])* math.cos(rad(27)))*scale
#     yP = (v[1]+(v[0]+v[2])* math.sin(rad(27)))*scale
#     xP += ox
#     yP += oy
#     return [xP,yP]
