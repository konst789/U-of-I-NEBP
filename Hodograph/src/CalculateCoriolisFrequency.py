# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 09:03:55 2023

@author: lkear
"""

import numpy as np
import OutputFormater as out

#Frequency is 2*rotatinalRatEarth*sin(lattitude) in rad/s
#Low frequency is 1/10x of high

def CalculateCoriolisFrequency (Lattitude,DoPrintOutput):
    out.pim("Begin CCF",DoPrintOutput)
    
    #Debug
    out.txt('Lattitude is '+str(Lattitude),DoPrintOutput)
    
    Lat = np.sin(Lattitude)
    pi = np.pi
    
    RotationalRate = (2*pi)/(86164.0905) #Sidereal Day in seconds, outputs in rad/s
    out.txt("Lat set to {L}, RotationalRate set to {R}".format(L=Lat,R=RotationalRate),DoPrintOutput)
    
    FrequencyLow = np.abs(2*RotationalRate*Lat)
    FrequencyHigh = FrequencyLow * 10
    
    #Debug
    out.txt("FrequencyHigh set to {X}".format(X=FrequencyHigh),DoPrintOutput)
    out.txt("FrequencyLow set to {Y}".format(Y=FrequencyLow),DoPrintOutput)
    
    out.pim("End CCF",DoPrintOutput)
    return (FrequencyHigh,FrequencyLow)