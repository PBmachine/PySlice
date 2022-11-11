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
from cmu_112_graphics import *
import psMeshimport as msh
import ps3D_render as rend
import numpy
import os

def getScale(app):
    box = numpy.subtract(testmesh.bbox[0],testmesh.bbox[1])
    scalexy = max(box[0],box[1])
    if scalexy >= box[2]:
        s = abs(.4*app.width/scalexy)
    else:
        print('use Z to scale')
        s = abs(.3*app.height/box[2])
    return s



def appStarted(app):
    app.Ox = app.width/2
    app.Oy = app.height*.77
    app.Cline = "cyan"
    app.Cbg = "black"
    app.projstyle = "iso"
    app.drawstyle = "wireframe"
    app.scale = getScale(app)
    app.rnd = rend.iso(27,[app.Ox,app.Oy],app.scale)
    app.wire = 1


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
    
def drawTriangle(app,canvas,pt):
    canvas.create_polygon(pt[0][0], pt[0][1], 
    pt[1][0], pt[1][1], pt[2][0], pt[2][1],
    outline = app.Cline, width = app.wire, fill = '')


def drawFacets(app,canvas):
    for i in range(testmesh.numfacets):
        face = testmesh.facets[i].v
        pts = numpy.zeros((3,2))
        for n in range(3):
            pts[n] = app.rnd.isoXY(face[n])
        drawTriangle(app,canvas,pts)

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    drawFacets(app,canvas)
    
    
    
def run3DViewer():
    print('Running 3D viewer... here goes nothing!')
    runApp(width=600, height=600)

#will need to put stl loader in the animation loop
cone96 = "pysliceMain\\Mesh_Models\\Cone_10x10_96_bin.stl"
bunny1 = "Mesh_Models\\bunny_lowpoly_bin.stl"

testmesh = msh.openSTL(bunny1)
print(testmesh.numfacets)
run3DViewer()