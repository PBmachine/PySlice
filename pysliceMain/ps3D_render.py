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
#rendering to make further back stuff less bright - like V is based on y and x value?
# allow for rotation and stuff
# uh ye
# """

import math
#https://www.compuphase.com/axometr.htm
def rad(degree):
    return math.radians(degree)

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
