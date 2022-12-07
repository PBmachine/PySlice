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
import psExport
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
    app.renderWindow = ui.window([5,5],[app.width*1-5,app.height*hb],
    app.styles["meshWindow"], 10)
    app.uiWindow = ui.window([5,app.height*hb], [app.width*1-5,app.height-5],
    app.styles["uiWindow"], 10)

    rbox = app.renderWindow
    rx = (rbox.ext[0]-rbox.origin[0])//2
    ry = (rbox.origin[1]+rbox.ext[1]-rbox.origin[1])*.75
    app.meshView = rnd.isoRender(app.renderWindow,[rx,ry],app.styles["mesh"])

    app.grid = rnd.createOgrid(app.renderWindow, app.meshView, app.styles["grid"],5)


def createButtons(app):
    style = app.styles["button1"]
    app.buttons=dict()
    
    #Button UI
    b=10 #button padding base dim
    a=50 #button height base dim
    
    app.buttons["sliceMesh"] = ui.button("sliceMesh",app.uiWindow, [b,b],[a*5,a],
    'sliceMesh(app)',style,"SLICE MESH")
    app.buttons["showhideslice"] = ui.button("hideslices",app.uiWindow, [b,b+b+a],[a*5,a],
    'showHide(app.slicerender)',style,"SHOW/HIDE SLICES")
    app.buttons["export"] = ui.button("export",app.uiWindow, [b,b+2*(b+a)],[a*5,a],
    'loadnextmesh(app)',style,"EXPORT SLICES")

    #2nd Column
    w=b*2+a*5
    app.buttons["incrh"] = ui.button("incrh",app.uiWindow, [w,b],[a*5,a],
    'incrx(app,.2)',app.styles["button2"],"INCREASE H")
    app.buttons["decrh"] = ui.button("decrh",app.uiWindow, [w,b+b+a],[a*5,a],
    'incrx(app,-.2)',app.styles["button2"],"DECREASE H")

    #3rd Column
    w=w+b+a*5
    app.buttons["loadNext"] = ui.button("loadNext",app.uiWindow, [w,b],[a*5,a],
    'loadnextmesh(app)',app.styles["button2"],"LD NEXT MESH")

    #deactivate until slices made
    app.buttons["export"].state = 0
   
    for key in app.buttons:
        app.uiWindow.objs[app.buttons[key].name] = app.buttons[key]


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
    app.fileExport = psExport.fileOutput("null",'sliceexport\\','CSV')


def loadMesh(app,meshfile,started = True):
    print(f'Loading {meshfile.name} mesh')
    style = app.styles["mesh"]
    app.cMesh = msh.openSTL(meshfile.filepath)
    app.cMesh.name = meshfile.name
    cMesh = rnd.meshObj(app.meshView,app.cMesh,style)
    app.renderWindow.objs["mesh"]=cMesh
    rnd.scale4Window(app.cMesh.bbox,app.meshView)

def loadnextmesh(app):
    if app.sliced:
        app.slicerender.render = False
    app.meshnum += 1
    if app.meshnum >= len(allmeshfiles):
        app.meshnum = 0
    loadMesh(app,allmeshfiles[app.meshnum])
    app.buttons["export"].state = 0

def reScale(app):
    scale =[app.width/app.WH[0],app.height/app.WH[1]]
    app.renderWindow.reScale(scale)
    app.uiWindow.reScale(scale)
    rnd.scale4Window(app.cMesh.bbox,app.meshView)
    for key in app.uiWindow.objs:
        app.uiWindow.objs[key].reScale(scale)
        # obj.origin[1] *= scale[1]
    app.WH = (app.width,app.height)

def keyPressed(app, event):
    if event.key == 'Right':
       app.meshView.addTheta(12.5,2)
    elif event.key == 'Left':
        app.meshView.addTheta(-12.5,2)
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
        app.param.h += .2
        if app.param.h >3:
            app.param.h = .2
        print(f'slice height = {app.param.h}')

def mouseReleased(app, event):
    if app.mouseCheck:
        print(f'mouseReleased at {(event.x, event.y)}')
        buttons = app.buttons
        pt = (event.x, event.y)
        app.mouseCheck = False
        for key in buttons:
            result = buttons[key].isPressed(pt)
            if result is not None:
                print(f'')
                for n in range(len(result)):
                    eval(result[n])

def incrx(app,x):
    app.param.h += x
    if app.param.h <= 0:
        app.parah.h = .2

def mousePressed(app, event):
    app.mouseCheck = True

def showHide(appobj):
    appobj.render = not(appobj.render)

def drawBackground(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill = app.Cbg)

def drawParam(app,canvas):
    style = app.styles['param']
    origin = app.renderWindow.origin

    text = f'Mesh: {app.cMesh.name}'
    canvas.create_text(origin[0]+10,origin[1]+10, text = text, 
            fill = style.fc, anchor = style.anchor,font = style.font)
    
    text = f'Slice Set: {round(app.param.h,2)}mm'
    canvas.create_text(origin[0]+10,origin[1]+28, text = text, 
            fill = style.fc, anchor = style.anchor,font = style.font)


def redrawAll(app, canvas):
    if app.WH != (app.width,app.height):
        reScale(app)
        app.WH = (app.width,app.height)
    drawBackground(app, canvas)
    app.renderWindow.draw(canvas)
    app.uiWindow.draw(canvas)
    app.grid.print = False
    drawParam(app,canvas)
    
    
def sliceMesh(app):
    app.meshslices = slicer.slicebyZ(app.cMesh,app.param.h)
    style = app.styles["slice"]
    app.slicerender = rnd.sliceObj(app.meshView,app.meshslices.slices,style)
    app.renderWindow.objs["slices"]=app.slicerender
    app.sliced = True
    app.buttons["export"].state = 1
    print(app.renderWindow.objs)
    
def export(app,data = []):
    if name == "null":
        name = app.cMesh.name
    if len(data)<=0:
        data = app.meshslices.slices


    
    app.fileExport.exportCSV
    
def run3DViewer():
    print('Running 3D viewer ...')
    runApp(width=800, height=800)

cone = meshFile("cone","Mesh_Models\\Cone_10x10_96_bin.stl")
bunny = meshFile("bunny","Mesh_Models\\bunny_lowpoly_bin.stl")
axolotl = meshFile("axolotl","Mesh_Models\\axolotl_lowpoly.stl")
sphere = meshFile("sphere","Mesh_Models\\sphere_10x10_180.stl")
donut = meshFile("donut","Mesh_Models\\donut.stl")
# trex = meshFile("trex","Mesh_Models\\Trex_Skull_lp.stl")
# frogchair = meshFile("frogchair","Mesh_Models\\frogchair.stl")
#Skull by Anthony at 3DP.org https://www.thingiverse.com/3p3d/designs
allmeshfiles = [bunny,cone,axolotl,sphere,donut]
# ,trex,frogchair]

def addMesh(name,filepath):
    newMesh=meshFile(name,filepath)
    allmeshfiles.append(newMesh)

default = bunny
defaultmesh = msh.openSTL(default.filepath)
h = 0.25


#test
run3DViewer()
#test
