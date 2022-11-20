###################################################
# Phoebe DeGroot
# PySlice Exporter v1_01: 20-11-22
#  ____   __  __   ____   __     __   ____   ______   
#  == ==  ==  ==  ==  -=  ==     ==  ==  -=  ==   -
#  ==  =  ==_ ==   -==    ==     ==  ==      ==-=
#  ====   _  ===  =   ==  ==     ==  ==   =  ==   _
#  ==      ====    ====   =====  ==   ====   ======  
# 
#information and methods for converting files to output format and saving
################################################### 

class postProcess(object):
    def __init__(self):
        #post processor class? unsure how to structure this
        pass
        #

class fileOutput(object):
    #file output - file suffix and save path
    def __init__(self,filetype,savepath):
        self.filetype = filetype
        self.savepath = savepath
        #

class Command(object):
    #commands for inserting into code
    def __init__(self,command):
        self.command = command
        pass

class textCommand(Command):
    #text based commands for inserting into code
    def __init__(self,command):
        super().__init__(command)
        pass
class machineCommand(Command):
    #machine command?
    def __init__(self,command):
        super().__init__(command)
        pass
class motionCommand(Command):
    #motion command
    def __init__(self,command):
        super().__init__(command)
        pass


        

#define output methods for turning the list of slices into code
#look at example Gcode post processors for info on structure


#list of coordinates,RAPID, GCode, extrusion type etc