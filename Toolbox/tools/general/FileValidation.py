'''
Created on Jul 31, 2014

@author: Adam
'''


import arcpy
import os

class FileValidation(object):
    '''
    classdocs
    '''
    @staticmethod
    def fileExists(theFile):
        
        if not os.path.isfile(theFile):
            raise ValueError('No Such File Exists')
            return False
        else:
            return True
        
    @staticmethod
    def isShape(theFile, shapeWanted):
        '''
        ex:
        shapeWanted = 'Point'
        '''
        desc = arcpy.Describe(theFile)
        
        shapeType = str(desc.shapeType)
        if shapeType != shapeWanted:
            raise TypeError('Input file not %s file, is: %s\n' % (shapeWanted,shapeType))
            return False
        else:
            return True
        
    @staticmethod
    def isUnits(theFile, unitsWanted):
        '''
        ex:
        unitsWanted = 'Meter'
        '''
        desc = arcpy.Describe(theFile)
        
        sr = desc.spatialReference
        unitsType = sr.linearUnitName
        if  unitsType != unitsWanted:
            raise TypeError('Input file not in %s unit, is: %s\n' % (unitsWanted,unitsType))
            return False
        else:
            return True