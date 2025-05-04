'''
Created on Jul 25, 2012

@author: Adam
'''


def isWithinDistance(p1, p2, distance_meters):
    distance_sq = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2
    
    if distance_sq <= distance_meters**2:
        return True
    else:
        return False
