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
import UIWidgets as ui

pi = math.pi

#https://www.compuphase.com/axometr.htm
def rad(degree):
    return math.radians(degree)

class trans:
    def __init__(self):
        self.theta = [0,0,0]
        self.shift = np.zeros((3,1))
    
def reOrient( pt, theta):
    #just gimbal, thanks
    Rx = np.matrix([[1,0,0],
    [0,math.cos(theta[0]),-1*math.sin(theta[0])],
    [0,math.sin(theta[0]),math.cos(theta[0])]])

    Ry= np.matrix([[math.cos(theta[1]),0,math.sin(theta[1])],
    [0,1,0],
    [-1*math.sin(theta[1]),0,math.cos(theta[1])]])

    Rz = np.matrix([[math.cos(theta[2]),-1*math.sin(theta[2]),0],
    [math.sin(theta[2]),math.cos(theta[2]),0],
    [0,0,1]])

    pt3d = np.asarray(pt)

    pt3d = np.reshape(pt3d,(3,))
    pt3d = np.asmatrix(pt3d)
    newpt = pt3d*Rx*Ry*Rz

    np.reshape(newpt,3)
    newpt = np.ravel(newpt)


    return(newpt)

        
def isoprojXY(pt, o, scale, a=27):
    a = math.radians(a)
    x = pt[0]*scale
    y = pt[1]*scale
    z = pt[2]*scale
    xP = o[0]+x*math.cos(a)-y*math.cos(a)
    yP = o[1]- x*math.sin(a) - y*math.sin(a) - z
    return([xP,yP])


class isoRender(object):
    def __init__(self,window,origin,style,scale = 1, theta = 0):
        self.window = window
        self.o = origin #XY origin
        self.scale = scale
        self.style = style
        self.a = math.radians(27)
        self.theta = np.zeros((3))
        self.objs=[]
        

    def addTheta(self,angle,index):
        angle = math.radians(angle)
        self.theta[index] = self.theta[index]+angle

    def projXY(self,pt1):
        np.asarray(pt1)
        pt = reOrient(pt1,self.theta)

        a = self.a
        x = pt[0]*self.scale
        y = pt[1]*self.scale
        z = pt[2]*self.scale
        xP = self.o[0]+x*math.cos(a)-y*math.cos(a)
        yP = self.o[1]- x*math.sin(a) - y*math.sin(a) - z

        return([xP,yP])

    def extBBox(self,bbox):
        
        ymin = self.projXY(bbox[0])[1]
        ymax = self.projXY(bbox[1])[1]
   
        xmin = self.projXY((bbox[0][0],bbox[1][1],bbox[0][0]))[0]
        xmax = self.projXY((bbox[1][0],bbox[0][1],bbox[0][0]))[0]
        w = np.array([[xmin,ymin],[xmax,ymax]])
        
        return(w)
    
    def scale2BBox(self,bbox,scale=0):
        window = self.window
        if scale == 0: scale = self.scale
        BBox = self.extBBox(bbox)
        w,h = abs(BBox[1][0]-self.o[0]),abs(BBox[1][1]-self.o[1])
        oratio = self.o[1]-BBox[0][0]
        wmin,hmin = abs(BBox[0][0]-self.o[0]),abs(BBox[0][1]-self.o[1])
        return(w,h,wmin,hmin,oratio)

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

    def draw(self, canvas):
        return

class obj3D(object):
    def __init__(self,isoRender,style, rescale = True, render = True):
        self.isoRender = isoRender
        if self not in isoRender.objs:
            isoRender.objs.append(self)
        self.style = style
        self.rescale = rescale #does object rescale with window
        self.render = render #activate/deactive render
        self.recalc = True #recalculate proj or use saved data
        self.drawdata = []
        self.savedtheta = self.isoRender.theta.copy()

class meshObj(obj3D):
    def __init__(self,isoRender,mesh,style, rescale = True, render = True):
        super().__init__(isoRender,style,rescale, render)      
        self.mesh= mesh

    def draw(self,canvas):
        if self.render == False:
            return
        mesh = self.mesh
        if self.recalc or not (np.allclose(self.savedtheta, self.isoRender.theta, rtol=1e-05, atol=1e-05, equal_nan=False)):
            self.recalc = True
            self.savedtheta = self.isoRender.theta.copy()
            # print(self.savedtheta)

        if self.recalc:
            self.drawdata = []
            for i in range(mesh.numfacets):
                face = mesh.nFacet(i).v
                pts = np.zeros((3,2))
                for n in range(3):
                    pts[n] = self.isoRender.projXY(face[n])
                self.drawTriangle(canvas,pts, self.style)
                self.drawdata.append(pts)
            self.recalc = False
        else:
            for n in range(len(self.drawdata)):
                self.drawTriangle(canvas,self.drawdata[n], self.style)

    def drawTriangle(self,canvas,pt, style):
        canvas.create_polygon(pt[0][0], pt[0][1], 
        pt[1][0], pt[1][1], pt[2][0], pt[2][1],
        outline = style.lc, width = style.lw, fill = style.fc, 
        stipple = style.stipple)
    

class lineObj(obj3D):
    #3D object defined by line segments - such as slices
    def __init__(self,isoRender,lines,style, rescale = True, render = True):
        super().__init__(isoRender,style,rescale, render)      
        self.lines= lines
        self.recalc=True
        self.drawdata = []
        self.savedtheta = self.isoRender.theta.copy()

    def draw(self,canvas):
        if self.render == False:
            return
        if not np.allclose(self.savedtheta, self.isoRender.theta, rtol=1e-05, atol=1e-05, equal_nan=False):
            self.recalc = True
            self.savedtheta = self.isoRender.theta.copy()

        if self.recalc:
            self.drawdata = []    
            for n in range(len(self.lines)):
                segment = self.lines[n]
                self.drawSegment(canvas,segment)
            self.recalc = False
        else:
            for n in range(len(self.drawdata)):
                self.drawLine(canvas,self.drawdata[n], self.style)
                

    def checkSegment(self):
        pass

    def drawSegment(self,canvas, segment):
        p1 = segment[0]
        np.asarray(p1)
        p2 = segment[1]
        np.asarray(p2)
        pts = np.zeros((2,2))

        pts[0] = self.isoRender.projXY(p1)
        pts[1] = self.isoRender.projXY(p2)
        self.drawdata.append(pts)

        self.drawLine(canvas,pts, self.style)

    def drawLine(self,canvas,pts,style):
        canvas.create_line(pts[0][0],pts[0][1],pts[1][0],pts[1][1], 
        fill = style.lc, width = style.lw, stipple = style.lstipple)

class sliceObj(lineObj):
    def draw(self,canvas):
        if self.render == False:
            return
        for slice in self.lines:
            for segment in slice.segments:
                self.drawSegment(canvas,segment)


def scale4Window(bbox, isoObj):
    #given window object and mesh bbox find scale and fit to window
    window = isoObj.window
    Mw, Mh, wmin,hmin,oratio = isoObj.gdimBBOX(bbox[0],bbox[1],scale = 1)
    # print(f'M:{Mw},{Mh},min:{wmin},{hmin}')
    #Mw, Mh, wmin,hmin,wratio = isoObj.scale2BBox(bbox,scale = 1)

    # wdims = window.dims()


    Wh = (window.ext[1]-window.origin[1])-window.margin*4
    Ww = (window.ext[0]-window.origin[0])-window.margin*4
    # print(f'M:{Mw},{Mh},min:{wmin},{hmin}')

    if (Mh/Wh >= Mw/Ww):
        #set by height
        scale = Wh/Mh
    else:
        scale = (Ww/Mw)

    oX = .5*Ww+scale*oratio + window.margin
    oY = Wh+window.margin-hmin*scale + window.margin
    origin = [oX,oY]

    isoObj.scale = scale
    isoObj.o = origin


    

def createOgrid(window,isoView,style,ext):
    segments = []
    w = ext
    for n in range(w):
        for m in range(-w+1,w):
            if m == 0:m=.1
            row = [[-n,m,0],[n,m,0]]
            col = [[m,-n,0],[m,n,0]]
            segments.append(row)
            segments.append(col)
    grid = lineObj(isoView,segments,style)
    window.objs["grid"] = grid

    return grid



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
