# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 18:29:12 2023

@author: lkear
"""

#Dependencies
import numpy as np
import pandas as pd
import OutputFormater as out

def InterpolateReIndex(DataInput,IndexOld,IndexNew,InterpStep,DoPrintOutput):
    """ 
    Data input is the Frame that you want to interpolate
    Index old is the index to compare the new values against
    Index New is the name of the index that you want to become the new reference
    Interp step is the distance between each point that you wanted interpolated
    DoPrintOutput is a boolean that determines if after each step it prints confirmation top console
    """
    
    #Debug info
    out.pim("Begining Interpolation", DoPrintOutput)
    out.txt("Old Index = {old}".format(old=IndexOld), DoPrintOutput)
    out.txt("New Index = {new}".format(new=IndexNew), DoPrintOutput)
    out.txt("Interpolation Step = {step}".format(step = InterpStep), DoPrintOutput)
    
    #Removes UTC before interpolating if it is in the data frame
    try:
        DataInput = DataInput.drop('UTC',axis=1)
    except:
        out.wrn('No UTC detected in profile',DoPrintOutput)
    
    #Import data tables of new data
    InterpReference = DataInput[str(IndexNew)]
    
    #Get Min/max of new index
    NewIndexMin = InterpReference.min()
    NewIndexMax = InterpReference.max()
    
    #setup for data
    dataInterpolated = pd.DataFrame() #new Frame for interpolated data
    
    # set min and max to be compatable with index
    # min is greater than acutal min and max is less that actual max to avoid problems with linear interpolation
    if ((NewIndexMin%InterpStep) != 0):
        NewIndexMin = NewIndexMin+(InterpStep - (NewIndexMin%InterpStep))
    if ((NewIndexMax%InterpStep) != 0):
        NewIndexMax = NewIndexMax-(NewIndexMax%InterpStep)
    #Debug Info
    out.txt('New Index Min is {min}'.format(min = NewIndexMin),DoPrintOutput)
    out.txt('New Index Max is {max}'.format(max = NewIndexMax),DoPrintOutput)
    
    #create an index for all values to interpolate on
    InterpolatedIndex = [*range(NewIndexMin,NewIndexMax+1,InterpStep)]
    
    #negative numbers represent less values in the new index, Debug Info
    out.txt('Old Index Length is {length}'.format(length = len(DataInput[str(IndexOld)])),DoPrintOutput)
    out.txt('New Index Length is {length}'.format(length = len(InterpolatedIndex)),DoPrintOutput)
    out.wrn("New Index will have {indexDiff} more values compared to old index".format(indexDiff=(len(InterpolatedIndex)-len(DataInput[str(IndexOld)]))), DoPrintOutput)
    
    #create first data column as index for interpolation of remaning data
    dataInterpolated[str(IndexNew)] = InterpolatedIndex
    
    #interp rest of data
    for col in DataInput.columns:
        if (str(col) != str(IndexNew)): #check to see that it is not the reference index
            out.txt("Interpolating {col}".format(col = col),DoPrintOutput)
            DataHold = DataInput[str(col)]
            dataInterpolated[str(col)] = np.interp(InterpolatedIndex,InterpReference,DataHold)
            out.scs("{col} Interpolated!".format(col = col),DoPrintOutput)
    
    out.pim("Data Linear Interpolation Completed",DoPrintOutput)
    return dataInterpolated
