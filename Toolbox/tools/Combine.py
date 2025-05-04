import arcpy
from adambebko.general.Centroid import Centroid


class CombineTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Combine Tool"
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
        
        identFieldParam = arcpy.Parameter(
                                 displayName="GPS Point ID Field",
                                 name="waypoint_ident",
                                 datatype="Field",
                                 parameterType="Required",
                                 direction="Input",
                                 )
        
        identFieldParam.filter.list = ['Text']
        identFieldParam.parameterDependencies = [inFileParam.name]
        identFieldParam.value = "IDENT"
        
        dateFieldParam = arcpy.Parameter(
                                 displayName="Datetime Field",
                                 name="waypoint_Datetime",
                                 datatype="Field",
                                 parameterType="Required",
                                 direction="Input",
                                 )
        
        dateFieldParam.filter.list = ['Date']
        dateFieldParam.parameterDependencies = [inFileParam.name]
        
        
        params = [inFileParam, identFieldParam, dateFieldParam ]
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
        identField = parameters[1].valueAsText
        messages.addMessage("InFile = " + inFile)
        
        identList = []
        coordsList = []
        
        with arcpy.da.SearchCursor(inFile, [identField, "SHAPE@XY"]) as cursor:  # @UndefinedVariable
            for row in cursor:
                identList.append(row[0])
                coordsList.append(row[1])
                messages.addMessage("ident = " + str(row[0]))
                messages.addMessage("coords = " +  str(row[1]))
        
        messages.addMessage("identList = " + str(identList))
        messages.addMessage("coordsList = " + str(coordsList))
        

        centroid = Centroid.getCentroid(coordsList)
        
        #TODO: Sort Ident. Right now it does stuff like 278-276 if you select 276 later on. Make sure to account for 998 999 001 002 etc..

        
        sorted(identList)
        identListMin = identList[0]
        identListMax = identList[len(identList)-1]
        newIdent = str(identListMin) +"-" + str(identListMax)
        
        messages.addMessage("newIdent = " + newIdent)

        firstRow = True
        with arcpy.da.UpdateCursor(inFile, [identField, "SHAPE@XY"]) as cursor:  # @UndefinedVariable
            for row in cursor:
                if firstRow:
                    row[0] = newIdent
                    row[1] = centroid
                    cursor.updateRow(row)
                    firstRow = False
                else:
                    cursor.deleteRow()
        
        with arcpy.da.SearchCursor(inFile, [identField, "SHAPE@XY"]) as cursor:  # @UndefinedVariable
            for row in cursor:
                messages.addMessage("ident = " + str(row[0]))
                messages.addMessage("coords = " +  str(row[1]))

        return