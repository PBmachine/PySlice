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
import csv



class fileOutput(object):
    #file output - file suffix and save path
    def __init__(self,filename,savepath,filetype):
        self.filetype = filetype
        self.savepath = savepath
        self.filename = filename
        self.header = []
        #

    def exportfile(self,data):
        if 'CSV' in upper(self.filetype):
            self.exportCSV(data)

#Citation: csv export - based on example from https://www.pythontutorial.net/python-basics/python-write-csv-file/
    def exportCSV(self,data):
        filepath = f'{self.filepath}{self.filename}'
        with open(filepath,'w',encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.header)
            writer.writerows(data)


#code 

class postProcess(object):
    def __init__(self):
        #post processor class 
        pass
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