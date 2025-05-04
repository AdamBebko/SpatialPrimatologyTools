
import arcpy
import Vectors, distance, timedifferencemin, speed, ToDatetime
import datetime

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [SpeedCalculation]

class SpeedCalculation(object):
    def __init__(self):
        """Calculating Tool"""
        self.label = "SpeedCalculation"
        self.description = "SpeedCalculation"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
#         
        inFileParam = arcpy.Parameter(
                                 displayName="Input Feature",
                                 name="in_feature",
                                 datatype="GPFeatureLayer",
                                 parameterType="Required",
                                 direction="Input",
                                 )
         
        datetimeField = arcpy.Parameter(
                                 displayName="DateTime Field",
                                 name="datetimeField",
                                 datatype="Field",
                                 parameterType="Required",
                                 direction="Input",
                                 )
        datetimeField.filter.list = ['Text']
        datetimeField.parameterDependencies = [inFileParam.name]
        
        durField = arcpy.Parameter(
                                 displayName="Duration Field",
                                 name="DurField",
                                 datatype="Field",
                                 parameterType="Optional",
                                 direction="Input",
                                 )
        durField.filter.list = ['Short']
        durField.parameterDependencies = [inFileParam.name]
        
        datetimeEndField = arcpy.Parameter(
                                 displayName="DateTime End Field",
                                 name="datetimeEndField",
                                 datatype="Field",
                                 parameterType="Optional",
                                 direction="Input",
                                 )
        datetimeEndField.filter.list = ['Text']
        datetimeEndField.parameterDependencies = [inFileParam.name]

        params = [inFileParam, datetimeField, durField, datetimeEndField]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        inFile = parameters[0].valueAsText
        arcpy.AddMessage("InFile = " + inFile)
        
        dateTimeField = parameters[1].valueAsText
        arcpy.AddMessage("date field = " + dateTimeField)
        
        durField = parameters[2].valueAsText 
        if not durField:
            arcpy.AddMessage("dur field not entered")
        else:
            arcpy.AddMessage("dur field = " + durField)
        
        datetimeEndField = parameters[3].valueAsText 
        if not datetimeEndField:
            arcpy.AddMessage("datetimeendfield  not entered")
        else:
            arcpy.AddMessage("datetimeendfield field = " + datetimeEndField)

        arcpy.AddMessage("adding speed field")
        arcpy.AddField_management(inFile, "SPEED","FLOAT")
        arcpy.AddMessage("finished adding speed field")
        

        cursorFieldList = ["SHAPE@XY", dateTimeField, "SPEED"]
        if durField:
            cursorFieldList.append(durField)
        if datetimeEndField:
            cursorFieldList.append(datetimeEndField)
 
 
        firstTimeThrough = True
        lastRow = None
        with arcpy.da.UpdateCursor(inFile, cursorFieldList) as cursor: # @UndefinedVariable
            for row in cursor:
                if firstTimeThrough:
                    lastRow = row
                    firstTimeThrough = False
                else:
                    coordsThis = row[0]
                    coordsLast = lastRow[0]
                    thisRowStartTime = ToDatetime.toDatetime(row[1])
                    lastRowStartTime = ToDatetime.toDatetime(lastRow[1])
                    
                    
#                     arcpy.AddMessage(str(coordsThis) + str(coordsLast))
#                     arcpy.AddMessage(str(thisRowStartTime)+ str(lastRowStartTime))
                                     
                    
                    vector = Vectors.subtract(coordsThis, coordsLast)
                    d = distance.distance(vector[0],vector[1])
                    
                    arcpy.AddMessage("dist = "+str(d))
                    timediff = timedifferencemin.timeDifferenceMin(thisRowStartTime, lastRowStartTime)
                    if durField:
                        lastRowDur =  lastRow[3]
                        timediff = timediff - lastRowDur
                        arcpy.AddMessage("timediff subtract duration of "+str(lastRowDur))
                    if datetimeEndField:
                        if durField:
                            pass
                        else:
                            lastRowEndTime = ToDatetime.toDatetime(row[4])
                            lastRowDur = timedifferencemin.timeDifferenceMin(lastRowEndTime, lastRowStartTime)
                            timediff = timediff - lastRowDur
                            arcpy.AddMessage("timediff subtract duration of = "+str(lastRowDur))
                            
                            
                    arcpy.AddMessage("timediff = "+str(timediff))
                    
                    if timediff <1:
                        thisSpeed = 0
                    else:
                        thisSpeed = speed.calspeed(d, timediff)
                    arcpy.AddMessage("speed = "+str(thisSpeed))
                    
                    row[2] = thisSpeed
                    cursor.updateRow(row)
                    lastRow = row
                    
            return        

#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
#     
