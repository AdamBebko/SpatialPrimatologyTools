import os, datetime
import arcpy


def convDate(comment, messages):
    #Converts Garmin date/time field to a datetime object
    day = int(comment[0:2])
    monthText = comment[3:6]
    if monthText == "JAN":
        month = 1
    elif monthText == "FEB":
        month = 2
    elif monthText == "MAR":
        month = 3
    elif monthText == "APR":
        month = 4
    elif monthText == "MAY":
        month = 5
    elif monthText == "JUN":
        month = 6
    elif monthText == "JUL":
        month = 7
    elif monthText == "AUG":
        month = 8
    elif monthText == "SEP":
        month = 9
    elif monthText == "OCT":
        month = 10
    elif monthText == "NOV":
        month = 11
    elif monthText == "DEC":
        month = 12
    else:
        print "month not recognized"
    year = 2000+int(comment[7:9])
    
    timeStart = comment.find(":")-2
    hour = int(comment[timeStart:timeStart+2])
    
    minute = int(comment[timeStart+3:timeStart+5])
    
    second = int(comment[timeStart+6:timeStart+8])

    if comment[-2:] == "PM" and hour != 12:
        hour += 12
        

    theDate = datetime.datetime(year, month, day, hour, minute, second)
    return theDate

class PrepGPSmap60cs(object):
    def __init__(self):
        """Test Tool"""
        self.label = "PrepRawGPSMap60cs"
        self.description = "PrepRawGPSMap60cs"
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
        
        dateFieldParam.filter.list = ['Text', 'Date']
        dateFieldParam.parameterDependencies = [inFileParam.name]
        dateFieldParam.value = "COMMENT"
        
        nameParam = arcpy.Parameter(
                                 displayName="Orangutan Name",
                                 name="orang_name",
                                 datatype="GPString",
                                 parameterType="Required",
                                 direction="Input",
                                 )
        
        fullDayParam = arcpy.Parameter(
                                 displayName="Full Day of Observation",
                                 name="fullday",
                                 datatype="GPBoolean",
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
        
        params = [inFileParam, identFieldParam, dateFieldParam, nameParam, fullDayParam, outFileParam]
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
        messages.addMessage("inFile = " + inFile)
        
        identField = parameters[1].valueAsText
        messages.addMessage("identField = " + identField)
        
        dateField = parameters[2].valueAsText
        messages.addMessage("dateField = " + dateField)
        
        orangName = parameters[3].valueAsText
        messages.addMessage("orangName = " + orangName)
        
        fullday = parameters[4].valueAsText
        messages.addMessage("fullday = " + fullday)
        
        outFile = parameters[5].valueAsText
        messages.addMessage("outFile = " + outFile)
        
        inDesc = arcpy.Describe(inFile)
        inShapeFieldName = inDesc.ShapeFieldName
        
        if fullday == "true":
            fullday = 1
        else:
            fullday = 0
            
            
            
        outPathTupule = os.path.split(outFile)    
           
        #scan input data 
        dataList = []
        with arcpy.da.SearchCursor(inFile, [inShapeFieldName, identField, dateField]) as cursor:  # @UndefinedVariable
            for row in cursor:
                rowsDate = convDate(row[2], messages)
                messages.addMessage(rowsDate.strftime("%Y %m %d %H:%M:%S"))
                dataRow = [row[0], row[1], rowsDate]
                dataList.append(dataRow)
                
        
        #Ensure data all from one date
        lastDate = None
        for dataRow in dataList:
            thisDate = dataRow[2]
            if lastDate:
                if str(thisDate)[:10] != str(lastDate)[:10]:
                    messages.addErrorMessage("more than one date present in input file")
                    messages.addWarningMessage("Program will still complete normally. However, an error will be listed to ensure this is intended.")
                    break
            else:
                lastDate = thisDate
        
        #sort list by date to make 999 followed by 001        
        dataList.sort(key=lambda x: x[2])
        
        #Ensure no large gaps in observation. If two consective waypoints are more than 45m apart flag a warning.
        lastTime = None
        numGaps = 0
        gapReports = []
        for dataRow in dataList:
            thisTime = dataRow[2]
            if lastTime:
                timeDiff = thisTime - lastTime
                if timeDiff.seconds > 45*60:
                    numGaps += 1
                    gapReports.append("Large Gap, "+ lastTime.strftime("%H:%M:%S") + ", " + thisTime.strftime("%H:%M:%S"))
            lastTime = thisTime
        if numGaps > 0:
            messages.addErrorMessage(str(numGaps) + " Gaps greater than 45m in data found")
            for gapReport in gapReports:
                messages.addWarningMessage(gapReport)
            messages.addWarningMessage("Program will still complete normally. However, an error will be listed to ensure this is intended.")
                
        
        #Create output file
        sr = arcpy.SpatialReference("WGS 1984 UTM Zone 50N")
        arcpy.CreateFeatureclass_management(outPathTupule[0], outPathTupule[1], "POINT", spatial_reference=sr)
        
        #Add fields to output file
        arcpy.AddField_management(outFile, "IDENT", "TEXT")
        arcpy.AddField_management(outFile, "DATE_", "DATE")
        arcpy.AddField_management(outFile, "DATETIME", "TEXT")
        arcpy.AddField_management(outFile, "ORANGUTAN", "TEXT")
        arcpy.AddField_management(outFile, "FULLDAY", "SHORT")
        
        #populate rows of output file
        cursor = arcpy.da.InsertCursor(outFile, ("SHAPE@", "IDENT", "DATE_", "DATETIME", "ORANGUTAN", "FULLDAY"))  # @UndefinedVariable
        for dataRow in dataList:
            rowsDate = dataRow[2]
            rowsDate_ = rowsDate.strftime("%m/%d/%Y")
            rowsDatetime = rowsDate.strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.insertRow((dataRow[0], dataRow[1], rowsDate_, rowsDatetime, orangName, fullday))
            
        del cursor
        
        return
    
    
    
    
    
    
    
    
    
    
    
    
