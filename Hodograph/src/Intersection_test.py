# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 10:12:11 2023

@author: lkear
"""
import numpy as np
import pandas as pd
import OutputFormater as out

#1 Integrate forward off of point
#2 detect if the points pass each other
#3 Check bv2 for that run
#4 if Valid, mark the point as complete and run it backwards to check
#5 advance point and repeat for dataset
#6 return list of good hits as start point and run length

def DetectIntersections(data,DoPrintOutput):
    out.pim("Begining Intersection Detection",DoPrintOutput)
    
    MinimumRun = 10
    MaximumRun = 1000
    
    RawData = pd.DataFrame()
    RawData['U'] = data['Ufiltered']
    RawData['V'] = data['Vfiltered']
    
        
    # IntersectionData = pd.DataFrame()
    # IntersectionData['U'] = data['Ufiltered']
    # IntersectionData['V'] = data['Vfiltered']
    
    # Ulist = IntersectionData['U'].tolist()
    # CalcHoldU = [0]
    # CalcHoldU[0] = 0
    # for x in range(1,len(IntersectionData['U'])):
    #     CalcHoldU.append(CalcHoldU[x-1]+Ulist[x])
    #     pass
    
    # Vlist = IntersectionData['V'].tolist()
    # CalcHoldV = [0]
    # CalcHoldV[0] = 0
    # for x in range(1,len(IntersectionData['V'])):
    #     CalcHoldV.append(CalcHoldV[x-1]+Vlist[x])
    #     pass
    
    # #Intersection detection test
    # TestHold = []
    # for x in range(0,1000):
    #     Greater = True
    #     TestHold.append(Ulist[int(x)])
    #     if (Greater == True)&(Ulist[int(x)] < Vlist[int(x+1)]):
    #         print(Ulist[int(x)])
    #         Greater = False
    #     print(int(x))
        
    out.pim("Intersection Detection Finished",DoPrintOutput)
    return 1