'''
Created on Jul 25, 2012

@author: Adam
'''
import WithinDistance


def getClusters(pointList, distance):
    '''
    Method that returns a list of clusters from a set of point objects with attributes x and y (pointlist).
    distance is the cutoff boundary for a cluster
    Each cluster is a list containing the indexes of the points making up the cluster
    '''
    
    clusters = []
    cluster = []
    lastPoint = None
    firstClusterPoint = None
    for index, point in enumerate(pointList):
        if lastPoint:
            
            #Check to see if testing against last point or the first point found in the cluster
            if firstClusterPoint:
                testPoint = firstClusterPoint
            else:
                testPoint = lastPoint
                
            #Check if current point is within distance of testpoint
            if WithinDistance.isWithinDistance(point,testPoint["Point"],distance):
                if len(cluster) == 0:
                    firstClusterPoint = testPoint
                    
                if testPoint["Index"] not in cluster:
                    cluster.append(testPoint["Index"])
                cluster.append(index)
            
            #if not within distance, add the cluster if it exists
            else:
                if len(cluster) > 0:
                    clusters.append(cluster)
                    cluster = []
                    firstClusterPoint = None
        lastPoint = {"Point":point, "Index":index}
    
    #if a cluster is left at end, add it.
    if len(cluster) > 0:
        clusters.append(cluster)
        cluster = []
    
    return clusters

        
    