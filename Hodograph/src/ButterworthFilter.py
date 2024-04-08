# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:27:34 2023

@author: lkear
"""

from scipy import signal
import OutputFormater as out

def UVButterworth(data,FilterOrder,InputMethod,High,Low,fs,DoPrintOutput):
    out.pim("Begin Butterworth",DoPrintOutput)
    
    #Debug
    out.txt("Input Method set to {x}".format(x=InputMethod),DoPrintOutput)
    out.txt("Filter order set to {x}".format(x=FilterOrder),DoPrintOutput)
    out.txt("High input set to {x}".format(x=High),DoPrintOutput)
    out.txt("Low input set to {x}".format(x=Low),DoPrintOutput)
    
    #Input method to hz
    if(InputMethod == 'hour'):
        #Target high frequency in hours (1/x*3600hz)
        FrequencyHigh = 1/(High*3600)
        FrequencyLow = 1/(Low*3600)
        
    elif(InputMethod == 'hz'):
        FrequencyHigh = High
        FrequencyLow = Low

    #Set Bandrange
    bandrange = [FrequencyLow,FrequencyHigh] #Target frequency typicaly ranges between 30min to 10 hr
    
    #Debug
    out.txt("Low Frequency set to {LF}hz".format(LF =bandrange[0]),DoPrintOutput)
    out.txt("High Frequency set to {HF}hz".format(HF =bandrange[1]),DoPrintOutput)

    #Create Butterworth Filter
    sos = signal.butter(FilterOrder, bandrange, 'bp', fs=fs, output='sos') #filter order, bandrange , bandpass, 1hz, output as sos
    out.txt("Butterworth Filter Created",DoPrintOutput)

    #Filtering the data
    datafiltered = signal.sosfilt(sos, data)
    out.scs("Data Filtered",DoPrintOutput)

    out.pim("Butterworth Filter Completed",DoPrintOutput)
    return datafiltered