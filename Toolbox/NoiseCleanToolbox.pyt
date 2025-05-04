import arcpy
import Clusters
import Centroid
import os
import ToDatetime
import timedifferencemin

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Noise Clean Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Noise Clean"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        inFileParam = arcpy.Parameter(
                                 displayName="Input Feature",
                                 name="in_feature",
                                 datatype="GPFeatureLayer",
                                 parameterType="Required",
                                 direction="Input")
        
        identFieldParam = arcpy.Parameter(
                                 displayName="GPS Point ID Field",
                                 name="waypoint_ident",
                                 datatype="Field",
                                 parameterType="Required",
                                 direction="Input")
        
        identFieldParam.filter.list = ['Text']
        identFieldParam.parameterDependencies = [inFileParam.name]
        
        datetimeFieldParam = arcpy.Parameter(
                                 displayName="Datetime Field",
                                 name="waypoint_Datetime",
                                 datatype="Field",
                                 parameterType="Required",
                                 direction="Input")
        
        datetimeFieldParam.filter.list = ['Text']
        datetimeFieldParam.parameterDependencies = [inFileParam.name]
        


        booleanContainsTrueFields = arcpy.Parameter(
                                displayName='Boolean Contains True Fields',
                                name='booleanContainsTrueFields',
                                datatype='Field',
                                parameterType='Optional',
                                direction='Input',
                                )
        
        booleanContainsTrueFields.parameterDependencies = [inFileParam.name]


        params = [inFileParam, identFieldParam, datetimeFieldParam, booleanContainsTrueFields]
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
                  
        identField = parameters[1].valueAsText
        datetimeField = parameters[2].valueAsText
        
        arcpy.AddMessage('Starting cluster method')
         
        booleanField = parameters[3].valueAsText
        if booleanField:
            arcpy.AddMessage("boolean Field:"+str(booleanField))
#          
#         try:
#             FileValidation.fileExists(inFile)
#             FileValidation.isShape(inFile, 'Point')
#             FileValidation.isUnits(inFile, 'Meter')
#         except TypeError, e:
#             arcpy.AddError("Problem with file type", e)
#         except ValueError, e:
#             arcpy.AddError(e)
        
        
        fieldList = ["SHAPE@XY", identField, datetimeField]
        if booleanField:
            fieldList.append(booleanField)
        #Get a list of points
        coordsList = []
        identsList = []
        datesList = []
        booleanList = []
        with arcpy.da.SearchCursor(inFile, fieldList) as cursor: #@UndefinedVariable
            for row in cursor:
                coordsList.append(row[0])
                identsList.append(row[1])
                datesList.append(row[2])
                if booleanField:
                    booleanList.append(row[3])
                        
                
        

        clusterList = Clusters.getClusters(coordsList, 20)
        arcpy.AddMessage(clusterList)
        

        durFieldName = "DUR_MIN"
        clusterFieldName = "CLUSTER"
        datetimeEndFieldName = "TIME_END"
        arcpy.AddField_management(inFile, durFieldName, "SHORT")
        arcpy.AddField_management(inFile, clusterFieldName, "SHORT")
        arcpy.AddField_management(inFile, datetimeEndFieldName , "TEXT", "", "", 20)

        fieldList2 = ["SHAPE@XY", identField, datetimeField, durFieldName, clusterFieldName, datetimeEndFieldName]
        if booleanField:
            fieldList2.append(booleanField)
        
        i = 0
        currentCluster = -1
        with arcpy.da.UpdateCursor(inFile, fieldList2) as cursor: #@UndefinedVariable
            for row in cursor:
                arcpy.AddMessage("working on row: "+str(i))
                thisCluster = None
                for j, cluster in enumerate(clusterList):
                    arcpy.AddMessage("looking at :"+ str(i)+"in: "+str(cluster))
                    if i in cluster:
                        thisCluster = j
                        
                if thisCluster or thisCluster == 0: 
                    arcpy.AddMessage("Row is in a cluster")
                    row[4] = 1
                    arcpy.AddMessage("currentCluster = "+ str(currentCluster) + "this cluster" + str(thisCluster))
                    if thisCluster != currentCluster:
                    #First time on this cluster, update row with cluster info
                        arcpy.AddMessage("Row is first point in a cluster, updating as centroid")
                        currentCluster = thisCluster
                        
                        
                        coords = []
                        idents = []
                        dates = []
                        boolean = 0
                        for clusterPointIndex in clusterList[currentCluster]:
                            arcpy.AddMessage(coordsList[clusterPointIndex])
                            coords.append(coordsList[clusterPointIndex])
                            idents.append(identsList[clusterPointIndex])
                            dates.append(datesList[clusterPointIndex])
                            if booleanField:
                                if booleanList[clusterPointIndex] == 1:
                                    boolean = 1
                            
                        centroid = Centroid.getCentroid(coords)
                        
                        firstIdent = idents[0]
                        lastIdent = idents[len(idents)-1]
                        ident = str(firstIdent) +"-"+ str(lastIdent)
                        arcpy.AddMessage(ident)
                        
                        firstDate = ToDatetime.toDatetime(dates[0])
                        lastDate = ToDatetime.toDatetime(dates[len(dates)-1])
                        dur = timedifferencemin.timeDifferenceMin(lastDate, firstDate)
                        
                        if booleanField:
                            row[len(fieldList2)-1] = boolean
                        
                        row[0] = centroid
                        row[1] = ident
                        row[3] = dur
                        row[5] = str(lastDate)
                        

                        
                        cursor.updateRow(row)
                            
                        
                    else:
                    #same cluster, can delete
                        arcpy.AddMessage("Row not first point in a cluster, deleting...")
                        cursor.deleteRow()
                else:
                    #Skip this row since not in cluster
                    row[3] = 0
                    row[4] = 0
                    
                    cursor.updateRow(row)
                    arcpy.AddMessage("Row is NOT in a cluster")
                    
                 
                i = i+1

# 
#                 newName = inFile + "_Cleaned"
#                 arcpy.AddMessage(inFile+newName)
#                 arcpy.Rename_management(inFile, newName)
        return