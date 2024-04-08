# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 10:02:36 2023

@author: lkear
"""

import matplotlib.pyplot as plt
import pandas as pd
import OutputFormater as out

def macroHodo(Alt,u,v):
    """ plot hodograph for entire flight
    """
    #plot v vs. u
    plt.figure("Macroscopic Hodograph", figsize=(10,10),dpi=120)  #Plot macroscopic hodograph
    plt.suptitle("Macro Hodograph for Entire Flight \n Background Wind Removed")
    c=Alt
    plt.scatter( u, v, c=c, cmap = 'magma', s = 1, edgecolors=None, alpha=1)
    cbar = plt.colorbar()
    cbar.set_label('Altitude')  
    return


#old UV plotting code
# fig = plt.figure(figsize=(16,9),dpi=120)
# plt.plot(data['Alt'], data['Ufiltered'], label = "U Filtered")
# plt.plot(data['Alt'], data['Vfiltered'], label = "V Filtered")
# plt.title("U & V Butterworth filter")
# plt.xlabel('Altitude (Meters)')
# plt.ylabel('m/s')
# plt.legend()
# plt.show()