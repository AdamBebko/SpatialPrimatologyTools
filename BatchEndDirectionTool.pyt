import arcpy
import os
import math

def unitvector(coords):
    length = math.sqrt(coords[0]**2 + coords[1]**2)
    newX = coords[0]/length
    newY = coords[1]/length
    newCoords=[newX, newY]
    return newCoords

def scale(coords, scalar):
    x= coords[0] * scalar
    y = coords[1] * scalar
    return [x,y]

def translate(coords, transVector):
    x =coords[0] + transVector[0]
    y = coords[1] + transVector[1]
    return [x,y]

def subtract(b, a):
    x = b[0]-a[0]
    y = b[1]-a[1]
    return [x,y]


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "EndDirection"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]



class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "End Direction Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        inFileParam = arcpy.Parameter(
                                 displayName="Input Feature",
                                 name="in_feature",
                                 datatype="GPFeatureLayer",
                                 parameterType="Required",
                                 direction="Input",
                                 )

        outFileParam = arcpy.Parameter(
                                 displayName="Output File",
                                 name="ouput_file",
                                 datatype="GPFeatureLayer",
                                 parameterType="Required",
                                 direction="Output",
                                 )
        
        params = [inFileParam,outFileParam]
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
        
        indivName = "ORANGUTAN"
        messages.addMessage("indivName = " + indivName)
        
        dateField = "DATE_"
        messages.addMessage("dateField = " + dateField)
        
        lostDay = "LOST_POINT"
        messages.addMessage("lostDay = " + lostDay)
        
        outFile = parameters[1].valueAsText
        messages.addMessage("outFile = " + outFile)
        
        date = None
        name = None
        lostDayVal = None
        coordsList = []
        with arcpy.da.SearchCursor(inFile, ["SHAPE@XY", indivName, dateField, lostDay]) as cursor: #@UndefinedVariable
            for row in cursor:
                if not date:
                    date = row[2]
                if not name:
                    name = row[1]
                if not lostDayVal:
                    lostDayVal = row[3]
                    
                coordsList.append(row[0])
              
        avgList= []      
                
        if len(coordsList) >= 1:        
            lastPoint = coordsList[len(coordsList)-1]
            
        if len(coordsList) >= 2:
            secondLastPoint = coordsList[len(coordsList)-2]
            avgList.append(secondLastPoint)
            #calculate first Line
            v1 =  subtract(lastPoint, secondLastPoint)
            v1_unit = unitvector(v1)
            v1_scaled = scale(v1_unit, 50)
            v1_end = translate(lastPoint, v1_scaled)
            a1 = arcpy.Array([arcpy.Point(lastPoint[0], lastPoint[1]), arcpy.Point(v1_end[0], v1_end[1])])            
            
        if len(coordsList) >= 3:
            thirdLastPoint = coordsList[len(coordsList)-3]
            avgList.append(thirdLastPoint)
            #calculate second Line
            v2 =  subtract(lastPoint, thirdLastPoint)
            v2_unit = unitvector(v2)
            v2_scaled = scale(v2_unit, 50)
            v2_end = translate(lastPoint, v2_scaled)
            a2 = arcpy.Array([arcpy.Point(lastPoint[0], lastPoint[1]), arcpy.Point(v2_end[0], v2_end[1])])
            
        if len(coordsList) >= 4:
            fourthLastPoint = coordsList[len(coordsList)-4]
            avgList.append(fourthLastPoint)
            #calculate third Line
            v3 =  subtract(lastPoint, fourthLastPoint)
            v3_unit = unitvector(v3)
            v3_scaled = scale(v3_unit, 50)
            v3_end = translate(lastPoint, v3_scaled)
            a3 = arcpy.Array([arcpy.Point(lastPoint[0], lastPoint[1]), arcpy.Point(v3_end[0], v3_end[1])])
            
        
        pAvgX = 0
        pAvgY = 0
        i = 0
        for point in avgList:
            pAvgX = pAvgX + point[0]
            pAvgY = pAvgY + point[1]
            i=i+1
        
        if i != 0:
            pAvgX = pAvgX/i
            pAvgY = pAvgY/i
        
        pAvg = [pAvgX, pAvgY]
        
        #calculate avg Line
        vAvg =  subtract(lastPoint, pAvg)
        vAvg_unit = unitvector(vAvg)
        vAvg_scaled = scale(vAvg_unit, 50)
        vAvg_end = translate(lastPoint, vAvg_scaled)
        
        aAvg = arcpy.Array([arcpy.Point(lastPoint[0], lastPoint[1]), arcpy.Point(vAvg_end[0], vAvg_end[1])])
        

        
        outPathTupule = os.path.split(outFile)    
        #Create output file

        
        outCursor = None
        try:
            # Create the output feature class
            #
            sr = arcpy.SpatialReference("WGS 1984 UTM Zone 50N")
            arcpy.CreateFeatureclass_management(outPathTupule[0], outPathTupule[1], "POLYLINE", spatial_reference=sr)
            
            #Add fields to output file
            arcpy.AddField_management(outFile, "NAME", "TEXT", "", "", 15)
            arcpy.AddField_management(outFile, "DATE_", "DATE")
            arcpy.AddField_management(outFile, "LOST_DAY", "SHORT")
            arcpy.AddField_management(outFile, "END_VECT", "TEXT", "", "", 5)
        
            # Open an insert cursor for the new feature class
            outCursor = arcpy.da.InsertCursor(outFile, ["SHAPE@", "NAME", "DATE_", "LOST_DAY", "END_VECT"]) #@UndefinedVariable
            
            if len(coordsList) >= 2:   
                outCursor.insertRow([arcpy.Polyline(a1), name, date, lostDayVal, 1])
            if len(coordsList) >= 3:   
                outCursor.insertRow([arcpy.Polyline(a2), name, date, lostDayVal, 2])
            if len(coordsList) >= 4:   
                outCursor.insertRow([arcpy.Polyline(a3), name, date, lostDayVal, 3])
            if i != 0:   
                outCursor.insertRow([arcpy.Polyline(aAvg), name, date, lostDayVal, "Avg"])
        
        
        except Exception as e:
            print e.message
        finally:
            # Cleanup the cursor if necessary
            #
            if outCursor:
                del outCursor
        
        return