###################################################
# Phoebe DeGroot
# PySlice App Event Handler
#  ____   __  __   ____   __     __   ____   ______   
#  == ==  ==  ==  ==  -=  ==     ==  ==  -=  ==   -
#  ==  =  ==_ ==   -==    ==     ==  ==      ==-=
#  ====   _  ===  =   ==  ==     ==  ==   =  ==   _
#  ==      ====    ====   =====  ==   ====   ======  
# 
###################################################       

mousepressed = False

def mouseReleased(app,event):
    if mousepressed:
        mousepressed = False
        buttons = app.buttons
        pt = (event.x, event.y)
        for key in buttons:
            result = buttons[key].isPressed(pt)
            if result is not None:
                result(app)

        return None

def mousePressed(app,event):
    mousepressed = True
    pass