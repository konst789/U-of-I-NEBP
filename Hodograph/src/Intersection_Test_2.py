# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 09:38:56 2023

@author: lkear
"""

import numpy as np
import OutputFormater as out

def findDistance (x,y,doPrintOutput):
    #function to find the distances of the x and y points in a set
    out.pim("Start of calculate all distances",doPrintOutput)
    
    distanceX = []
    distanceY = []
    i=0
    
    for i in range(len(x)-1):
        
        distanceX.append(abs(x[i]-x[i+1]))
        distanceY.append(abs(y[i]-y[i+1]))
        
        #debug
        #out.txt("Index {z0} returned distance {z1}".format(z0=i,z1=distance[i]),doPrintOutput)
    out.txt("Max distance X {i}".format(i=max(distanceX)),doPrintOutput)
    out.txt("Min distance X {i}".format(i=min(distanceX)),doPrintOutput)
    out.txt("Max distance Y {i}".format(i=max(distanceY)),doPrintOutput)
    out.txt("Min distance Y {i}".format(i=min(distanceY)),doPrintOutput)         
    out.pim("End of calculate all distances",doPrintOutput)
    return(distanceX,distanceY)

def checkIntersection (x1,y1,x2,y2,x3,y3,x4,y4):
    #Takes line segments A,B and the max distance that the x and y can be apart and determines if they intersect
    
    #Check to see if intersection is possible
    isValidIntersection = False
    if max(x1,x2) < min(x3,x4):
        if max(x3,x4) < min(x1,x2):
            if max(y1,y2) < min(y3,y4):
                if max(y3,y4) < min(y1,y2):
                    isValidIntersection = True
    
    if isValidIntersection == True:
        #Prepare var for intersection testing
        if x1 < x2:
            x1,y1,x2,y2 = x2,y2,x1,y1
        if x3 < x4:
            x3,y3,x4,y4 = x4,y4,x3,y3
        if y1 < y3:
            x1,x2,x3,x4 = x3,x4,x1,x2
            y1,y2,y3,y4 = y3,y4,y1,y2
        
        #Detect intersection
        if(x1>=x2)&(x1>=x4)&(x3>=x2)&(x3>=x4):
            if(y1>=y2)&(y1>=y4)&(y3>=y2)&(y3>=y4):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
  
def checkIntercept(x,y,doPrintOutput):
    distanceX,distanceY = findDistance(x,y,doPrintOutput)
    
    xMax = max(distanceX)
    yMax = max(distanceY)
    dataLength = len(x)
    maxRun = 1500 # defined by maximum frequency
    minRun = 130 #defined by minimum frequency
    Filtered = []
    
    for i in range(dataLength-1):
        #print(i)
        for j in range(dataLength - i):
            if (j > maxRun):
                break
            elif (abs(x[i]-x[i+j]))<=xMax:
                if (abs(y[i]-y[i+j]))<=yMax:
                    if minRun < ((i+j) - i):
                        Filtered.append(i+j)
    
    out.txt("Filtered list {i} values long".format(i=len(Filtered)),doPrintOutput)         
    #Filtered = set(list(Filtered)) #Remove Duplicate Values
    Filtered = np.unique(Filtered) #Remove Duplicate Values
    out.txt("Duplicates Removed Filtered list {i} values long".format(i=len(Filtered)),doPrintOutput)   
    
    Intersections = []
    
    for i in range(len(Filtered)-1):
        for j in range(len(Filtered) - i):
            
            x1 = x[i]
            y1 = y[i]
            
            x2 = x[i+1]
            y2 = y[i+1]
            
            x3 = x[i+j]
            y3 = y[i+j]
            
            x4 = x[i+j+1]
            y4 = y[i+j+1]
            
            if checkIntersection(x1, y1, x2, y2, x3, y3, x4, y4) == True:
                Intersections.append(Filtered(i))
                out.txt("Intersection detected at index {z}".format(z=i), doPrintOutput)
            else:
                Intersections.append(-1)
        pass
    Intersections = np.unique(Intersections) #Remove Duplicate Values
    
    return(Filtered,Intersections)
        