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
import UIWidgets as ui
import numpy
import math
import psSlicer as slicer

class meshFile(object):
    def __init__(self,name,filepath):
        self.name = name
        self.filepath = filepath

class sliceparam(object):
    def __init__(self,h):
        self.h = h


def setWindows(app):
    hb = .75
    app.window = dict()
    app.renderWindow= ui.window([10,10],[app.width*1-10,app.height*hb],
    app.styles["meshWindow"], 10)
    app.uiWindow = ui.window([10,app.height*hb], [app.width*1-10,app.height],
    app.styles["uiWindow"], 10)

    rbox = app.renderWindow
    rx = (rbox.ext[0]-rbox.origin[0])//2
    ry = (rbox.origin[1]+rbox.ext[1]-rbox.origin[1])*.75
    app.meshView = rnd.isoObj(app.renderWindow,[rx,ry],app.styles["mesh"])
    app.renderWindow.objs.append(app.meshView)


def appStarted(app):
    #starting mesh
    app.meshnum = 0
    app.WH = (app.width, app.height)
    app.slicerender = False
    app.styles = ui.defaultStyles()
    setWindows(app)
    loadMesh(app,allmeshfiles[app.meshnum])
    app.Cbg = "black"
    app.param = sliceparam(.25)

def loadMesh(app,meshfile):
    print(f'Loading {meshfile.name} mesh')
    app.cMesh = msh.openSTL(meshfile.filepath)
    app.meshView.objs.append(app.cMesh)
    rnd.scale4Window(app.cMesh.bbox,app.meshView)

def reScale(app):
    scale =[app.width/app.WH[0],app.height/app.WH[1]]
    app.renderWindow.ext[0] = app.width-10
    app.renderWindow.ext[1] *=scale[1]
    app.uiWindow.origin[0] = app.width-10
    app.uiWindow.origin[1] *= scale[1]
    rnd.scale4Window(app.cMesh.bbox,app.meshView)
    app.WH = (app.width,app.height)


def keyPressed(app, event):
    if event.key in ['Up', 'Right']:
       print("No function yet!")
    elif (event.key in ['Down', 'Left']):
        print("No function yet!")
    elif event.key == 'm':
        print(f"run slicer at constant height:{app.param.h}")
        app.meshslices = sliceMesh(app.cMesh,app.param.h)
        app.slicerender = True
    elif event.key == 'c':
        print("clear slicer")
        app.slicerender = False
    elif event.key == 'n':
        #load next mesh
        app.slicerender = False
        app.meshnum += 1
        if app.meshnum >= len(allmeshfiles):
            app.meshnum = 0
        loadMesh(app,allmeshfiles[app.meshnum])
    elif event.key == 'h':
        #change h by .25 increments
        app.param.h += .25
        if app.param.h >1.5:
            app.param.h = .25
        print(f'slice height = {app.param.h}')

def drawCircle(app,canvas,x0,y0,r,style):
    #helper fn from hw3- draws circle on center x0,y0 with radius r
    canvas.create_oval(x0-r, y0-r, x0+r, y0+r, 
    fill = style.f, outline = style.l, width = style.w)

def drawLine(canvas,pts,style):
    canvas.create_line(pts[0][0],pts[0][1],pts[1][0],pts[1][1], fill = style.lc, width = style.lw)

def drawGrid(app,canvas):
    #use this to draw the base grid, major axes and origin
    pass
    # for r in range(len(app.board)):
    #     for c in range(len(app.board[0])):
    #         drawCell(app,canvas, r, c, app.board[r][c])
    

def drawTriangle(canvas,pt, style):
    canvas.create_polygon(pt[0][0], pt[0][1], 
    pt[1][0], pt[1][1], pt[2][0], pt[2][1],
    outline = style.lc, width = style.lw, fill = style.fc, 
    stipple = style.stipple)

def drawFacets(app,canvas,mesh, isoView):
    for i in range(mesh.numfacets):
        face = mesh.nFacet(i).v
        pts = numpy.zeros((3,2))
        for n in range(3):
            pts[n] = isoView.projXY(face[n])
        drawTriangle(canvas,pts, app.styles["mesh"])

def drawMesh(app,canvas):
    #drawMeshbackground


    app.renderWindow.draw(canvas,False)
    drawFacets(app, canvas, app.cMesh, app.meshView)

def drawSlices(app,canvas,isoView):
    style = app.styles["slice"]
    for slice in app.meshslices.slices:
        for segment in slice.segments:
            p1 = segment[0]
            p2 = segment[1]
            pts = numpy.zeros((3,2))

            pts[0] = isoView.projXY(p1)
            pts[1] = isoView.projXY(p2)
            drawLine(canvas,pts, style)

def drawBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = app.Cbg)

def redrawAll(app, canvas):
    if app.WH != (app.width,app.height):
        reScale(app)
        app.WH = (app.width,app.height)
    drawBackground(app, canvas)
    drawMesh(app,canvas)
    if app.slicerender == True:
        drawSlices(app,canvas,app.meshView)
    
def sliceMesh(mesh,zh):
    data = slicer.slicebyZ(mesh,zh)
    return data

    
def run3DViewer():
    print('Running 3D viewer ...')
    runApp(width=800, height=800)

cone = meshFile("cone","Mesh_Models\\Cone_10x10_96_bin.stl")
bunny = meshFile("bunny","Mesh_Models\\bunny_lowpoly_bin.stl")
anglebox = meshFile("anglebox","Mesh_Models\\box_12_bin.stl")
testbox = meshFile("testbox","Mesh_Models\\defaultbox_bin.stl")
sphere = meshFile("sphere","Mesh_Models\\sphere_10x10_180.stl")
donut = meshFile("donut","Mesh_Models\\donut.stl")
allmeshfiles = [bunny,cone,sphere,donut,anglebox,testbox]

def addMesh(name,filepath):
    newMesh=meshFile(name,filepath)
    allmeshfiles.append(newMesh)

default = bunny
defaultmesh = msh.openSTL(default.filepath)
h = 0.25


#test
run3DViewer()
#test
