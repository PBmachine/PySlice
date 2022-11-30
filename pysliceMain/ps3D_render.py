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
# 
###################################################

#reorg iso class
# 
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
        
def isoprojXY(pt, o, scale, a=27):
    a = math.radians(a)
    x = pt[0]*scale
    y = pt[1]*scale
    z = pt[2]*scale
    xP = o[0]+x*math.cos(a)-y*math.cos(a)
    yP = o[1]- x*math.sin(a) - y*math.sin(a) - z
    return([xP,yP])




    




def dimXY(v,ox,oy,scale):
    #dimetric projection of xyz coord to x,y coord
    xP = (v[0]*math.cos(rad(7))+(v[1]*math.cos(rad(42)))/2) * scale
    yP = (v[1]+(v[1]*math.sin(rad(42)))/2-v[0]*math.sin(rad(7))) * scale
    xP += ox
    yP += oy
    return [xP,yP]


def dimBBOX(Pmin,Pmax,scale=1,a = 27):
    #gets the w and h of object in current projection
    #use scale = 1 to get overall dims to set view scale
    #delta = Pmax - Pmin #for numpy arrays 
    a = math.radians(a)
    dX = round(Pmax[0]-Pmin[0],1)
    dY = round(Pmax[1]-Pmin[1],1)
    dZ = round(Pmax[2]-Pmin[2],1)
    


    w = abs((dX*math.cos(a)+dY*math.cos(a))) * scale
    h = abs((dX*math.sin(a)+dY*math.sin(a)+dZ)) * scale
    hmin = ((0-Pmin[0])*math.sin(a)+(0-Pmin[1])*math.sin(a)+0-Pmin[2])

    oratio = (dY*math.cos(a)/w)
    return (w,h,oratio,hmin)

def dimBBOX(Pmin,Pmax,scale=1,a = 27):
    #gets the w and h of object in current projection
    #use scale = 1 to get overall dims to set view scale
    #delta = Pmax - Pmin #for numpy arrays 
    a = math.radians(a)
    dX = round(Pmax[0]-Pmin[0],1)
    dY = round(Pmax[1]-Pmin[1],1)
    dZ = round(Pmax[2]-Pmin[2],1)
    print(f'dx = {dX}, dy = {dY}, dz = {dZ}')

    w = abs((dX*math.cos(a)+dY*math.cos(a))) * scale
    h = abs((dX*math.sin(a)+dY*math.sin(a)+dZ)) * scale
    print(f'width={w}, height = {h}')

    oratio = (dY*math.cos(a)/w)
    return (w,h,oratio)
# OLD
# def isoXY(v,ox,oy,scale):
#     #isometric projection of xyz coord to x,y coord
#     xP = ((v[0]-v[2])* math.cos(rad(27)))*scale
#     yP = (v[1]+(v[0]+v[2])* math.sin(rad(27)))*scale
#     xP += ox
#     yP += oy
#     return [xP,yP]
