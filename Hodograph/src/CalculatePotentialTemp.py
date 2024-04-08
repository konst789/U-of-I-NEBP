# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:11:27 2023

@author: lkear
"""
import OutputFormater as out

def CalculatePotentialTemperature (CurrentTempC,ReferencePressure,ParcelPressure,DoPrintOutput):
    out.pim('Begin Potential Temperature Calculation',DoPrintOutput)
    
    #Convert to Kelvin
    CurrentTempK = CurrentTempC + 274.15
    
    #Calculate Potential Temperature
    PotentialTemperature = CurrentTempK*((ReferencePressure/ParcelPressure)**(0.286))
    
    out.pim('Potential Temperature Calculation Complete',DoPrintOutput)
    return PotentialTemperature