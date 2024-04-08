# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:29:13 2023

@author: lkear
"""


import numpy as np
import pandas as pd
from scipy import signal

import OutputFormater as out

def CalculateUV(data,DoPrintOutput):
    #Calculate u,v
    radial = -data.Wd*np.pi/180
    out.scs('Radial Data Calculated',DoPrintOutput)
    
    U = data.Ws * np.cos(radial)
    out.scs('U Calculated',DoPrintOutput)
    
    V = data.Ws * np.sin(radial)
    out.scs('V Calculated',DoPrintOutput)
    
    #Join U,V to dataframe 'data'
    data['U'] = U.tolist()
    data['V'] = V.tolist()
    return(data)