#################################################
#  ____   __  __   ____   __     __   ____   ______   
#  == ==  ==  ==  ==  -=  ==     ==  ==  -=  ==   -
#  ==  =  ==_ ==   -==    ==     ==  ==      ==-=
#  ====   _  ===  =   ==  ==     ==  ==   =  ==   _
#  ==      ====    ====   =====  ==   ====   ======  
#                           
# main
# 
#################################################
import psApp 
import os
import psSlicer as slicer
import psMeshimport as msh



cone96 = "Mesh_Models\\Cone_10x10_96_bin.stl"
bunny1 = "Mesh_Models\\bunny_lowpoly_bin.stl"
anglebox = "Mesh_Models\\box_12_bin.stl"
testbox = "Mesh_Models\\defaultbox_bin.stl"
sphere = "Mesh_Models\\sphere_10x10_180.stl"
donut = "Mesh_Models\\donut.stl"

filepath = donut
mesh = msh.openSTL(filepath)
h = 0.5
#test
# psApp.run3DViewer(mesh)
slicer.slicebyZ(mesh,h)