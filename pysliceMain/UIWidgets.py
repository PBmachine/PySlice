###################################################
# Phoebe DeGroot
#  ____   __  __   ____   __     __   ____   ______   
#  == ==  ==  ==  ==  -=  ==     ==  ==  -=  ==   -
#  ==  =  ==_ ==   -==    ==     ==  ==      ==-=
#  ====   _  ===  =   ==  ==     ==  ==   =  ==   _
#  ==      ====    ====   =====  ==   ====   ======  
# 
################################################### 
# Implement ToDo:
#
# Low: Handler for latching button events:
################################################### 
from tkinter import *
##>classes------------------------------------------------------------------
class window(object):
    #a canvas in tkinter
    def __init__(self, origin, ext, style, margin = 5):
        self.origin = origin
        self.ext = ext
        self.style = style
        self.margin = margin
        self.objs = []
        

    def draw(self, canvas, drawobjs = True):
        style = self.style
        canvas.create_rectangle(self.origin[0],self.origin[1],
        self.ext[0],self.ext[1], outline = style.lc, width = style.lw, 
        fill = style.fc)
        #draw all objects in the window
        if drawobjs: self.drawobjs(canvas)

    def drawobjs(self,canvas):
        for obj in self.objs:
            obj.draw(canvas)

##>>style-----------------------------------
class style(object):
    def __init__(self,fillc,linec,lineweight, smooth = 0, stipple = "", linestipple = "",
    fontc = "white", anchor = "CENTER", font = ('Consolas','12')):
        self.fc = fillc
        self.lc = linec
        self.lw = lineweight
        self.smooth = smooth
        self.stipple = stipple
        self.lstipple = linestipple
        self.fontc = fontc
        self.anchor = anchor
        self.font = font

class UIobj(object):
    def __init__(self, name, window, origin,style, dims = [], **tags):
        self.name = name
        self.origin =[origin[0] + window.origin[0],origin[1] + window.origin[1]]
        self.window = window
        self.style = style #copy? 
        self.dims = dims
        self.clickEvents = []
        self.tags = tags

    def getBounds(self, shape = "rectangle"):
        if shape == "rectangle":
            objx0 = self.origin[0]
            objy0 = self.origin[1]
            objx1 = objx0+self.dims[0]
            objy1 = objy0+self.dims[1]
            return([[objx0,objy0],[objx1,objy1]])
        

##>>button-----------------------------------
class button(object):
    def __init__(self, name, window, origin, dims, event,
     style, text = "", **tags):
        super().__init__(name, window, origin, style, dims, tags)
        self.state = 1 #1 or -1 for up and down, 0 for inactive
        self.text = text
        self.clickEvents = [event]
        self.resizeFont()
        self.bounds = self.getBounds()

    def resizeFont(self):
        #autoresize font to button height
        yheight = (self.dims[1]*.8)//1
        self.style.font[1] = yheight

    def inBounds(self,pt):
        bounds= self.bounds
        if (bounds[1][0]-pt[0]>bounds[0][0]) and (bounds[1][1]-pt[1]>bounds[0][1]):
            return True
        else:
            return False

    def isPressed(self,pt):
        if self.state == 0:
            return None
        if self.inBounds(pt):
            return self.clickEvents
        else:
            return None

    def hover(self,pt):
        #highlight button under cursor
        if self.state == 0:
            return
        if self.inBounds(pt):
            self.highlight()

    def draw(self,canvas):
        style = self.style

        if self.state ==0:
            stipple = "gray25"
            outline = "grey"
            lstipple = stipple
        else:
            stipple = style.stipple
            outlinec = style.lc
            lstipple = style.lstipple

        canvas.create_rectangle(self.origin[0],self.origin[1],
        self.dims[0],self.dims[1], outline = outlinec, width = style.lw, 
        fill = style.fc, stipple = stip, outlinestipple = lstipple)

        if len(self.text>0):
            center = [self.dims[0]-self.origin[0]/2,self.dims[1]-self.origin[1]/2]
            canvas.create_text(center[0],center[1], text = self.text, 
            fill = style.fontc, font = style.font)

##>methods------------------------------------------------------------
def defaultStyles():
    styles = dict()
    styles["meshWindow"] = style("black","cyan",5)
    styles["slice"] = style("","green2",1)
    styles["mesh"] = style("cyan4","cyan3",1,stipple = "gray25")
    styles["uiWindow"] = style("black","cyan",5)
    return styles
