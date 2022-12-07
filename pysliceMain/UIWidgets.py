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
import copy
##>classes------------------------------------------------------------------
class window(object):
    #a canvas in tkinter
    def __init__(self, origin, ext, style, margin = 5):
        self.origin = origin
        self.ext = ext
        self.style = style
        self.margin = margin
        self.objs = dict()

    def dims(self):
        return(self.ext[0]-self.origin[0],self.ext[1]-self.origin[1])

    def inBounds(self,pt):
        o = self.origin
        ext = self.ext
        if ((pt[0]>o[0]) and (pt[0]<ext[0])) and ((pt[1]>o[1]) and (pt[1]<ext[1])):
            return True
        else:
            return False
        
    def draw(self, canvas, drawobjs = True):
        style = self.style
        canvas.create_rectangle(self.origin[0],self.origin[1],
        self.ext[0],self.ext[1], outline = style.lc, width = style.lw, 
        fill = style.fc)
        #draw all objects in the window
        if drawobjs: self.drawobjs(canvas)

    def reScale(self,scale):
        for n in range(2):
            self.origin[n] *= scale[n]
            self.ext[n] *= scale[n]

    def drawobjs(self,canvas):
        for key in self.objs:
            self.objs[key].draw(canvas)


##>>style-----------------------------------
#palette
p= {"HotPink":"#f652a0","TiffanyBlue":"#bcece0",
"Cyan":"#36eee0","CyanDk":"#00A3A3","CyanLt":"#8AFFFF",
"CoralLt":"#ff9b69","Coral":"#f07143", "CoralDk":'#c4533d',
"LilacLt":'#d3bbdd','LilacDk':'#977397','Lilac':'#b195bd'}

def defaultStyles():
    styles = dict()
    styles["meshWindow"] = style("black",p['Cyan'],5)
    styles["slice"] = style("","green2",1)
    styles["mesh"] = style(p['CyanDk'],p['CyanDk'],1,["gray25",""])
    styles["grid"] = style("","SlateGray4",1,["gray50","gray50"])
    styles["uiWindow"] = style("black","cyan",5)
    styles["button1"] = style(p["Coral"],p["CoralLt"],2,["",""],c="black",a="center",font= ('Lucida Sans Typewriter','12',"bold"))
    styles["button2"] = style(p["CyanDk"],p['Cyan'],2,["",""],c="black",a="center",font= ('Lucida Sans Typewriter','12','bold'))
    styles["button3"] = style(p["Coral"],p["CoralLt"],2,["",""],c="black",a="center",font= ('Lucida Sans Typewriter','12','normal'))
    styles["param"] = style('white','white',1,["",""],c="white",a="nw",font= ('Lucida Sans Typewriter','12','normal'))
    return styles

class style(object):
    def __init__(self,fillc,linec,lineweight, stipple = ["",""], **text ):
        self.fc = fillc
        self.lc = linec
        self.lw = lineweight
        self.smooth = 0
        self.stipple, self.lstipple = stipple[0],stipple[1]
        self.tc,self.anchor,self.font = self.setFont(text)
    
    def setFont(self,text):
        default = ("black","CENTER",('Consolas','12'))
        if len(text)<=0 or text['c']=="":
            tc = "black"
            anchor = "CENTER"
            font = ('Consolas','12')
        else:
            tc = text['c']
            anchor = text['a']
            font = text['font']
        return(tc,anchor,font)


class UIobj(object):
    def __init__(self, name, window, origin,style, dims = [], *tags):
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

    def reScale(self,scale):
        for n in range(2):
            self.origin[n] *= scale[n]
            self.dims[n] *= scale[n]
        self.resizeFont()


class text(UIobj):
    def __init__(self, name, window, origin, 
     style, text ="",param=[],dims=[], **tags):
        super().__init__(name, window, origin, style, dims)
        self.state = 1 #1 or -1 for up and down, 0 for inactive
        self.text = text
        self.param = param

    def draw(self,canvas):
        style = self.style
        if self.state != 0:
            text = f'{self.text} {self.param}mm'
            canvas.create_text(self.origin[0],self.origin[1], text = text, 
            fill = style.fc, anchor = style.anchor,font = style.font)

    def resizeFont(self):
        return


    
##>>button-----------------------------------
class button(UIobj):
    def __init__(self, name, window, origin, dims, event,
     style, text = "", **tags):
        super().__init__(name, window, origin, style, dims)
        self.state = 1 #1 or -1 for up and down, 0 for inactive
        self.text = text
        self.clickEvents = [event]
        self.resizeFont()
        self.bounds = self.getBounds()
        


    def resizeFont(self):
        #autoresize font to button height
        aspect = abs(self.dims[0]/self.dims[1]/10)
        yheight = int((self.dims[1]*aspect)*.85)
        if len(self.text)>14:
            self.style = copy.copy(self.style)
            e = len(self.text)-14
            yheight = int(yheight- self.dims[1]/30*e)

        font = self.style.font
        if len(font)>=2:
            self.style.font = (font[0],str(yheight),font[2])
        else:
            self.style.font = (font[0],str(yheight))

    def inBounds(self,pt):
        o = self.origin
        ext = [self.origin[0]+self.dims[0],self.origin[1]+self.dims[1]]
        if ((pt[0]>o[0]) and (pt[0]<ext[0])) and ((pt[1]>o[1]) and (pt[1]<ext[1])):
            print(f'{self.name} pressed')
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
        ext = [self.origin[0]+self.dims[0],self.origin[1]+self.dims[1]]

        if self.state ==0:
            stipple = "gray25"
            outlinec = "black"
            lstipple = "gray25"
        else:
            stipple = style.stipple
            outlinec = style.lc
            lstipple = style.lstipple

        canvas.create_rectangle(self.origin[0],self.origin[1],
        ext[0],ext[1], outline = outlinec, width = style.lw, 
        fill = style.fc, stipple = stipple, outlinestipple = lstipple)

        if len(self.text)>0:
            center = [self.dims[0]/2+self.origin[0],self.dims[1]/2+self.origin[1]]
            canvas.create_text(center[0],center[1], text = self.text, 
            fill = style.tc, font = style.font)


def drawCircle(app,canvas,x0,y0,r,style):
    #helper fn from hw3- draws circle on center x0,y0 with radius r
    canvas.create_oval(x0-r, y0-r, x0+r, y0+r, 
    fill = style.f, outline = style.l, width = style.w)

def createButtons(app):
    style = app.styles["button1"]
    buttons=dict()
    
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
    return(buttons)