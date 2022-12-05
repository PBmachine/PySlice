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
    app.uiWindow = ui.window([10,app.height*hb], [app.width*1-10,app.height-10],
    app.styles["uiWindow"], 10)

    rbox = app.renderWindow
    rx = (rbox.ext[0]-rbox.origin[0])//2
    ry = (rbox.origin[1]+rbox.ext[1]-rbox.origin[1])*.75
    app.meshView = rnd.isoRender(app.renderWindow,[rx,ry],app.styles["mesh"])

    app.grid = rnd.createOgrid(app.renderWindow, app.meshView, app.styles["grid"],5)



def createButtons(app):
    style = app.styles["button1"]
    app.buttons=dict()
    app.buttons[sliceMesh] = ui.button(sliceMesh,app.uiWindow, [10,10],[250,50],
    sliceMesh,style,"SLICE MESH")
    app.buttons["loadNext"] = ui.button("loadNext",app.uiWindow, [10,70],[250,50],
    loadnextmesh,style,"LD NEXT MESH")
    app.buttons["export"] = ui.button("export",app.uiWindow, [10,70+60],[250,50],
    loadnextmesh,style,"EXPORT")
    #deactivate until slices made
    app.buttons["export"].state = 0
    
    
    for key in app.buttons:
        app.uiWindow.objs[app.buttons[key].name] = app.buttons[key]

def export(app):
    pass
def appStarted(app):
    #starting mesh
    app.meshnum = 0
    app.WH = (app.width, app.height)
    app.styles = ui.defaultStyles()
    setWindows(app)
    app.sliced = False
    createButtons(app)
    loadMesh(app,allmeshfiles[app.meshnum],False)
    app.Cbg = "black"
    app.param = sliceparam(.25)

def loadMesh(app,meshfile,started = True):
    print(f'Loading {meshfile.name} mesh')
    style = app.styles["mesh"]
    app.cMesh = msh.openSTL(meshfile.filepath)
    cMesh = rnd.meshObj(app.meshView,app.cMesh,style)
    app.renderWindow.objs["mesh"]=cMesh
    rnd.scale4Window(app.cMesh.bbox,app.meshView)

def reScale(app):
    scale =[app.width/app.WH[0],app.height/app.WH[1]]
    app.renderWindow.reScale(scale)
    app.uiWindow.reScale(scale)
    rnd.scale4Window(app.cMesh.bbox,app.meshView)
    for key in app.uiWindow.objs:
        app.uiWindow.objs[key].reScale(scale)
        # obj.origin[1] *= scale[1]
    app.WH = (app.width,app.height)

def loadnextmesh(app):
    if app.sliced:
        app.slicerender.render = False
    app.meshnum += 1
    if app.meshnum >= len(allmeshfiles):
        app.meshnum = 0
    loadMesh(app,allmeshfiles[app.meshnum])
    app.buttons["export"].state = 0

def keyPressed(app, event):
    if event.key in ['Up', 'Right']:
       print("No function yet!")
    elif (event.key in ['Down', 'Left']):
        print("No function yet!")
    elif event.key == 'm':
        print(f"run slicer at constant height:{app.param.h}")
        sliceMesh(app)
    elif event.key == 'c':
        print("show/hide slicer")
        app.slicerender.render =  not app.slicerender.render
    elif event.key == 'n':
        #load next mesh
        loadnextmesh(app)

    elif event.key == 'h':
        #change h by .25 increments
        app.param.h += .25
        if app.param.h >1.5:
            app.param.h = .25
        print(f'slice height = {app.param.h}')

def mouseReleased(app, event):
    print(f'mouseReleased at {(event.x, event.y)}')
    buttons = app.buttons
    pt = (event.x, event.y)
    for key in buttons:
        result = buttons[key].isPressed(pt)
        if result is not None:
            print(f'')
            for n in range(len(result)):
                result[n](app)



def drawBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = app.Cbg)

def redrawAll(app, canvas):
    if app.WH != (app.width,app.height):
        reScale(app)
        app.WH = (app.width,app.height)
    drawBackground(app, canvas)
    app.renderWindow.draw(canvas)
    app.uiWindow.draw(canvas)
    app.grid.print = False
    
    
    
def sliceMesh(app):
    app.buttons["export"].state = 0
    app.meshslices = slicer.slicebyZ(app.cMesh,app.param.h)
    style = app.styles["slice"]
    app.slicerender = rnd.sliceObj(app.meshView,app.meshslices.slices,style)
    app.renderWindow.objs["slices"]=app.slicerender
    app.sliced = True
    app.buttons["export"].state = 1

    
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
