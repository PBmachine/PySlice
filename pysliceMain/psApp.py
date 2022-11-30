###################################################
# Phoebe DeGroot
# PySlice App MVC v1_01: 20-11-22
#  ____   __  __   ____   __     __   ____   ______   
#  == ==  ==  ==  ==  -=  ==     ==  ==  -=  ==   -
#  ==  =  ==_ ==   -==    ==     ==  ==      ==-=
#  ====   _  ===  =   ==  ==     ==  ==   =  ==   _
#  ==      ====    ====   =====  ==   ====   ======  
# 
################################################### 
# To Do:
# reorganize classes for rendering, color, projection
#better scaling
###################################################
from cmu_112_graphics import *
import psMeshimport as msh
import ps3D_render as rnd
import numpy
import math

class window(object):
    def __init__(self,origin,w,h,margin, style):
        self.origin = origin
        self.w = w
        self.h = h
        self.margin = margin
        self.style = style

    def draw(self, app,canvas):
        style = self.style
        canvas.create_rectangle(self.origin[0],self.origin[1],
        self.w,self.h, outline = style.l, width = style.w, 
        fill = style.f)

class style(object):
    def __init__(self,fillc,linec,linew):
        self.f = fillc
        self.l = linec
        self.w = linew

class isoObj(object):
    def __init__(self,mesh,window,style):
        self.mesh = mesh
        self.window = window
        self.s, self.o = scale4Window(window,mesh.bbox)
        self.a = math.radians(27)
        self.style = style

    def projXY(self,pt):
        x = pt[0]*self.s
        y = pt[1]*self.s
        z = pt[2]*self.s
        xP = self.o[0]+x*math.cos(self.a)-y*math.cos(self.a)
        yP = self.o[1]- x*math.sin(self.a) - y*math.sin(self.a) - z
        return([xP,yP])

    def reScale(self):
        self.s,self.o = scale4Window(self.window,self.mesh.bbox)

def gdimBBOX(Pmin,Pmax,scale=1,a = 27):
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
    wmin = ((0-Pmin[0])*math.cos(a))*scale
    oratio = (dX*math.cos(a)/w)


    return (w,h,wmin,hmin,oratio)

def scale4Window(window, bBox):
    #given window object and mesh bbox find scale and fit to window
    Mw, Mh, wmin,hmin,wratio = gdimBBOX(bBox[0], bBox[1])
    Wh = window.h-window.margin*4
    Ww = window.w-window.margin*4
    if (Mh/Wh >= Mw/Ww):
        #set by height
        scale = Wh/Mh
    else:
        scale = (Ww/Mw)

    oX = wratio*Ww+wmin*scale*wratio + window.margin
    oY = Wh+window.margin-hmin*scale + window.margin

    origin = (oX,oY)
    return(scale,origin)


def appStarted(app):
    #starting mesh
    app.cMesh = msh.openSTL(default)
    app.WH = (app.width, app.height)
    meshRender = style("","cyan",1)
    meshBg = style("black","cyan",2)
    app.meshWindow = window((10,10),app.width*.8, app.height*.8,10, meshBg)
    app.meshV = isoObj(app.cMesh,app.meshWindow, meshRender)
    app.Cbg = "black"
    app.projstyle = "iso"

def drawCircle(app,canvas,x0,y0,r,fillColor, outwidth):
    #helper fn from hw3- draws circle on center x0,y0 with radius r
    canvas.create_oval(x0-r, y0-r, x0+r, y0+r, 
    fill = fillColor, outline = "black", width = app.outwidth)


def keyPressed(app, event):
    if event.key in ['Up', 'Right']:
       print("No function yet!")
    elif (event.key in ['Down', 'Left']):
        print("No function yet!")
    elif event.key == 'd':
        #dimetric
        app.projstyle = 'dim'
    elif event.key == 'i':
        #isometric
        app.projstyle = 'iso'

def drawBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = app.Cbg)

def drawGrid(app,canvas):
    #maybe use this to draw the base grid, major axes and origin
    pass
    # for r in range(len(app.board)):
    #     for c in range(len(app.board[0])):
    #         drawCell(app,canvas, r, c, app.board[r][c])
    
def drawTriangle(app,canvas,pt, style):
    canvas.create_polygon(pt[0][0], pt[0][1], 
    pt[1][0], pt[1][1], pt[2][0], pt[2][1],
    outline = style.l, width = style.w, fill = style.f)


def drawFacets(app,canvas,mesh, isoView):
    for i in range(mesh.numfacets):
        face = mesh.nFacet(i).v
        pts = numpy.zeros((3,2))
        for n in range(3):
            pts[n] = isoView.projXY(face[n])
        drawTriangle(app,canvas,pts, isoView.style)

def drawMesh(app,canvas):
    #drawMeshbackground
    if app.WH != (app.width,app.height):
        app.meshV.window.h = app.height*.8
        app.meshV.window.w = app.width*.9
        app.meshV.reScale()
        app.WH = (app.width,app.height)

    app.meshWindow.draw(app,canvas)
    drawFacets(app, canvas, app.cMesh, app.meshV)

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawMesh(app,canvas)
    
    
    
def run3DViewer():
    print('Running 3D viewer ...')
    runApp(width=800, height=800)

cone96 = "Mesh_Models\\Cone_10x10_96_bin.stl"
bunny1 = "Mesh_Models\\bunny_lowpoly_bin.stl"
font = "Mesh_Models\\pyslice_letters_bin.stl"
anglebox = "Mesh_Models\\box_12_bin.stl"
testbox = "Mesh_Models\\defaultbox_bin.stl"
default = bunny1
#test
run3DViewer()