'''
Created on Jul 25, 2012

@author: Adam
'''


def getCentroid(coords):
    sum_X = 0
    sum_Y = 0
    n = 0
    for coord in coords:
        try:
            sum_X += coord[0]
            sum_Y += coord[1]
            n += 1
        except:
            raise TypeError("Coordinates not in proper format")
    
    centroid_X = sum_X/n
    centroid_Y = sum_Y/n
    
    centroid = [centroid_X, centroid_Y]

    return centroid
        