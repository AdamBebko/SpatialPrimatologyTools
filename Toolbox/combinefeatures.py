'''
Created on Jul 26, 2012

@author: Adam
'''



class CombineFeatures(object):
    '''
    classdocs
    '''
    @staticmethod
    def concatenateList(dataList, delimiter=', '):
        outString = ''
        for data in dataList:
            dataString = str(data)
            outString += dataString + delimiter
        outString = outString[:-len(delimiter)]
        return outString
    
    @staticmethod
    def listRange(dataList):
        maximum = max(dataList)
        minimum = min(dataList)
        theRange = str(minimum) + ' - ' + str(maximum)
        return theRange
    
    @staticmethod
    def onlySame(dataList):
        different = False
        lastValue = None
        for data in dataList:
            if lastValue:
                if data != lastValue:
                    different = True
            lastValue = data
        if not different:
            return data
        else:
            return None
        
#     @staticmethod
#     def getCombinedRow(Rows, fields):
#         outRow = Adam_Row(fields)
#         for field in fields:
#             points = []
#             if field.type == 'Geometry': 
#                 for row in Rows:
#                     geom = (row.getValue(field.name))
#                     point = geom.getPart()
#                     points.append(point)
# 
#                 centroidPoint = Centroid.getCentroid(points)
#                 centroidGeom = arcpy.PointGeometry(centroidPoint)
#                 setattr(outRow, field.name, centroidGeom)
#                 
#             elif field.type != 'OID':
#                 values = []
#                 outValue = None
#                 for row in Rows:
#                     value = row.getValue(field.name)
#                     values.append(value)
#                 
#                 same = CombineFeatures.onlySame(values)
#                 if same:
#                     outValue = same
#                 else:
#                     outValue = CombineFeatures.concatenateList(values)
#                     
#                 setattr(outRow, field.name, outValue)
# 
#                     
#             
#         return outRow
#                 
#         
#         
            
            
            
        
    
    
    
    
    
    
    
    
    
    
    
    
    