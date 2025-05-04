
import arcpy
import os
#from general.FileValidation import FileValidation
#from general.Clusters import Clusters



class ClusterToolBox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ClusterMethod]


class ClusterMethod(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Cluster Method Tool"
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
        
#         identFieldParam = arcpy.Parameter(
#                                  displayName="GPS Point ID Field",
#                                  name="waypoint_ident",
#                                  datatype="Field",
#                                  parameterType="Required",
#                                  direction="Input",
#                                  )
#          
#         identFieldParam.filter.list = ['Text']
#         identFieldParam.parameterDependencies = [inFileParam.name]
#         identFieldParam.value = "IDENT"
#          
#         dateFieldParam = arcpy.Parameter(
#                                  displayName="Datetime Field",
#                                  name="waypoint_Datetime",
#                                  datatype="Field",
#                                  parameterType="Required",
#                                  direction="Input",
#                                  )
#         dateFieldParam.filter.list = ['Date']
#         dateFieldParam.parameterDependencies = [inFileParam.name]
#         
        
#         
        
        params = [inFileParam]
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
        
        outFile = parameters[1].valueAsText
        arcpy.AddMessage("outFile = " + outFile)
        #outPathTupule = os.path.split(outFile)  
        
        arcpy.AddMessage('Starting cluster method')
        
        try:
            #FileValidation.fileExists(inFile)
            #FileValidation.isShape(inFile, 'Point')
            #FileValidation.isUnits(inFile, 'Meter')
            arcpy.AddMessage('File Appears Valid')
        except TypeError, e:
            arcpy.AddError("Problem with file type", e)
        except ValueError, e:
            arcpy.AddError(e)
 
        #desc = arcpy.Describe(inFile)

        #inputFields = arcpy.ListFields(inFile)
        
        #Get a list of points
        try:
            coordsList = []
            with arcpy.da.SearchCursor(inFile, ["SHAPE@XY"]) as cursor: #@UndefinedVariable
                for row in cursor:
                    coordsList.append(row[0])
        except:
            raise
        finally:
            del row, cursor
        
        #clusterList = Clusters.getClusters(coordsList, 20)
        #arcpy.AddMessage(clusterList)
        
#         try:
#             #Create output file
#             sr = arcpy.SpatialReference("WGS 1984 UTM Zone 50N")
#             output = arcpy.CreateFeatureclass_management(outPathTupule[0], outPathTupule[1], "POINT", spatial_reference=sr)
#             
#             for field in inputFields:
#                 arcpy.AddField_management(outFile, field.name, field.type)
#     
#             
#         
#             clusterRows = []
#             i = 0
#             with arcpy.da.SearchCursor(inFile, ["SHAPE@XY"]) as cursor: #@UndefinedVariable
#                 for row in cursor:
#                     
#                     clusterPoint = None
#                     for cluster in clusterList:
#                         if i in cluster:
#                             clusterPoint = True
#                             
#                     if clusterPoint:
#                         clusterRows.append(row)
#                     else:
#                         if len(clusterRows) > 0:
# #                             newRow = CombineFeatures.getCombinedRow(clusterRows)
# #                             print ClusterRow.Shape.getPart()
# #                             outRow = outRows.newRow()
# #                             for field in ClusterRow.fields:
# #                                 outRow.setValue(field.name, ClusterRow.getValue(field.name))
# #                             outRows.insertRow(outRow)
# #                             clusterRows = []
# #                             
# #                         outRows.insertRow(row)
# #                     
#                     
#                     i = i+1
#         except:
#             raise
#         finally:
#             del row, cursor #TODO delete file if no worky
#             
#             
#             
#         for i, row in enumerate(inRows):
#             
#             
#                 
#             clusterPoint = None
#             
#             for cluster in clusterList:
#                 if i in cluster:
#                     clusterPoint = True
#                     
#             if clusterPoint:
#                 clusterRows.append(Adam_Row(inputFields, row=row))
#             else:
#                 if len(clusterRows) > 0:
#                     ClusterRow = CombineFeatures.getCombinedRow(clusterRows , inputFields)
#                     print ClusterRow.Shape.getPart()
#                     outRow = outRows.newRow()
#                     for field in ClusterRow.fields:
#                         outRow.setValue(field.name, ClusterRow.getValue(field.name))
#                     outRows.insertRow(outRow)
#                     clusterRows = []
#                     
#                 outRows.insertRow(row)
#                 
        
        return



