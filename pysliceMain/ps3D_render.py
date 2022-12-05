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


class isoObj(object):
    def __init__(self,window,origin,style,scale = 1):
        self.window = window
        self.o = origin #XY origin
        self.scale = scale
        self.style = style
        self.objs = []
        self.a = math.radians(27)

    def projXY(self,pt):
        a = self.a
        x = pt[0]*self.scale
        y = pt[1]*self.scale
        z = pt[2]*self.scale
        xP = self.o[0]+x*math.cos(a)-y*math.cos(a)
        yP = self.o[1]- x*math.sin(a) - y*math.sin(a) - z
        return([xP,yP])

    def gdimBBOX(self,Pmin,Pmax,scale=1):
        if scale == 0: scale = self.scale
        a = self.a
        dX = round(Pmax[0]-Pmin[0],3)
        dY = round(Pmax[1]-Pmin[1],3)
        dZ = round(Pmax[2]-Pmin[2],3)

        w = abs((dX*math.cos(a)+dY*math.cos(a))) * scale
        h = abs((dX*math.sin(a)+dY*math.sin(a)+dZ)) * scale
        hmin = ((0-Pmin[0])*math.sin(a)+(0-Pmin[1])*math.sin(a)+0-Pmin[2])
        wmin = ((0-Pmin[0])*math.cos(a))*scale
        oratio = (dX*math.cos(a)/w)

        return (w,h,wmin,hmin,oratio)


def scale4Window(bbox, isoObj):
    #given window object and mesh bbox find scale and fit to window
    window = isoObj.window
    Mw, Mh, wmin,hmin,wratio = isoObj.gdimBBOX(bbox[0], bbox[1],scale = 1)
    

    Wh = (window.ext[1]-window.origin[1])-window.margin
    Ww = (window.ext[0]-window.origin[0])-window.margin
    if (Mh/Wh >= Mw/Ww):
        #set by height
        scale = Wh/Mh
    else:
        scale = (Ww/Mw)

    oX = wratio*Ww+wmin*scale*wratio + window.margin
    oY = Wh+window.margin-hmin*scale + window.margin
    origin = (oX,oY)

    isoObj.scale = scale
    isoObj.o = origin


    




# def dimXY(v,ox,oy,scale):
#     #dimetric projection of xyz coord to x,y coord
#     xP = (v[0]*math.cos(rad(7))+(v[1]*math.cos(rad(42)))/2) * scale
#     yP = (v[1]+(v[1]*math.sin(rad(42)))/2-v[0]*math.sin(rad(7))) * scale
#     xP += ox
#     yP += oy
#     return [xP,yP]


# def dimBBOX(Pmin,Pmax,scale=1,a = 27):
#     #gets the w and h of object in current projection
#     #use scale = 1 to get overall dims to set view scale
#     #delta = Pmax - Pmin #for numpy arrays 
#     a = math.radians(a)
#     dX = round(Pmax[0]-Pmin[0],1)
#     dY = round(Pmax[1]-Pmin[1],1)
#     dZ = round(Pmax[2]-Pmin[2],1)
    


#     w = abs((dX*math.cos(a)+dY*math.cos(a))) * scale
#     h = abs((dX*math.sin(a)+dY*math.sin(a)+dZ)) * scale
#     hmin = ((0-Pmin[0])*math.sin(a)+(0-Pmin[1])*math.sin(a)+0-Pmin[2])

#     oratio = (dY*math.cos(a)/w)
#     return (w,h,oratio,hmin)

# def dimBBOX(Pmin,Pmax,scale=1,a = 27):
#     #gets the w and h of object in current projection
#     #use scale = 1 to get overall dims to set view scale
#     #delta = Pmax - Pmin #for numpy arrays 
#     a = math.radians(a)
#     dX = round(Pmax[0]-Pmin[0],1)
#     dY = round(Pmax[1]-Pmin[1],1)
#     dZ = round(Pmax[2]-Pmin[2],1)
#     print(f'dx = {dX}, dy = {dY}, dz = {dZ}')

#     w = abs((dX*math.cos(a)+dY*math.cos(a))) * scale
#     h = abs((dX*math.sin(a)+dY*math.sin(a)+dZ)) * scale
#     print(f'width={w}, height = {h}')

#     oratio = (dY*math.cos(a)/w)
#     return (w,h,oratio)
# OLD
# def isoXY(v,ox,oy,scale):
#     #isometric projection of xyz coord to x,y coord
#     xP = ((v[0]-v[2])* math.cos(rad(27)))*scale
#     yP = (v[1]+(v[0]+v[2])* math.sin(rad(27)))*scale
#     xP += ox
#     yP += oy
#     return [xP,yP]
