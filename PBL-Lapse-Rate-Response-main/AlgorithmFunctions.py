# -*- coding: utf-8 -*-
"""
Created on:  Wed Jun 30 12:03:33 2021
This program sets up all the functions for the PBL Conditional Generation

Section1: 
    -Runs starting calculations many of the functions require
        -Simplifies the need of running same calculation multiple times
    -Defines operation programs to run for Conditions and PBL methods
Section2:
    -3 primary PBL function methods
        -SH method ommitted after consistently most error prone
    -RI,PT,VPT methods generated
Section3:
    -3 Primary conditions are found
        -Nocturnal Layer Presense
        -Lower stability:VPT Gradient and Brunt-Vaisaila
        -Saturation from Humidity (>96%=Saturated)
    -Selection process for identifying PBL method based on conditions met above
        -If Nocturnal Layer: PT Method (reduced range to 200m)
        -If Saturated w/No nocturnal Layer: VPT
        -Else: RI 
Section4: 
    -Generates Full Output of all profiles run in current session
    -Outputs to console in clean layout
    -SaveTxt saves both clean layout and CSV for later processesing 


Last Updated: 10/9/2021 - 14:36PST

@author: Chambers,Alex
"""
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import time


def startingCalc(data):
    epsilon = 0.622          #[]
    virtcon = 0.61           #[]
    dwPt = data['Dewp.']     #[C]    
    hi = data['Alt'] - data['Alt'].iloc[0]               # subtract starting height for Above Ground Level (abl)
    e = np.exp(1.8096+(17.269425*dwPt)/(237.3+dwPt))     # vapor pressure
    rvv = (epsilon * e) / (data['P'] - e)                # water vapor mixing ratio []
    pot = (1000.0 ** 0.286) * (data['T'] + 273.15)\
        /(data['P'] ** 0.286)                            # potential temperature [K]
    vpt = pot * (1 + (virtcon * rvv))                    # virtual potential temperature [K]

    return hi,rvv,pot,vpt

def operations(data,saveName): 
#Run the following functions for full analysis and contain results in corresponding functions
    startData = startingCalc(data)
    Nocturnal = NoctLayer(data)
    Stability = lowerStability(startData,data)
    Humidity  = Hum(data)
    
    RI  = pblRI(startData,data)
    VPT = pblVPT(startData,saveName)
    PT  = pblPT(startData,Nocturnal)
    
    return RI,VPT,PT,Nocturnal,Stability,Humidity

######################################
########PBL FUNCTIONS#################
######################################

#NOTE: PBL values are commonly described as "[]" meters above surface 
#so all methods are corrected for height above gound

def pblRI(startData,data):
    hi = startData[0]       #[m]
    vpt= startData[3]       #[C]
    u = -data['Ws'] * np.sin(data['Wd'] * np.pi / 180)  #u component of wind 
    v = -data['Ws'] * np.cos(data['Wd'] * np.pi / 180)  #v component of wind
    g = 9.81  # m/s/s
    ri = (((vpt - vpt.iloc[0]) * hi * g) / (vpt.iloc[0] * (u ** 2 + v ** 2)))  #Bulk richardson number
    
    # Check for positive RI <= 0.25 and height between 100 and 3000 meters
    index = [100 <= a <= 0.25 and 0 <= b <= 3000 for a, b in zip(ri, hi)]  #

    if np.sum(index) > 0:  # Return results if any found
        return np.max(hi[index])

    # Otherwise, interpolate to find height
    index = [1 <= n <= 3000 for n in hi]  # Trim to interested range  
    hi = hi[index]
    ri = ri[index]
    
    return round(np.interp(0.25, ri, hi))    #linearly interpolate to critical RI value (.25)

def pblPT(startData,noct):
    ##nocturnal layers have a temp inversion. When tropopause inversion is stronger, the method chooses this value
    #Reducing depth when nocturnal layer is present isolates the range needed
    hi = startData[0]
    pot = startData[2]
    if noct ==1:
        topH = 500   #[m] - Upper limit to look for PBL
        lowH = 1     #[m] - Lower limit to look for PBL
    else:
        topH = 3000  #[m] - Upper limit to look for PBL
        lowH = 1     #[m] - Lower limit to look for PBL
    
    # Trim potential temperature and height to within specified heights
    heights = [i for i in hi if lowH <= i <= topH]
    pt = [p for p, h in zip(pot, hi) if lowH <= h <= topH]
    
    dp = np.gradient(pt,heights)                #gradient of potential temp with height
    arr = np.array(heights)[dp == np.max(dp)]   #get height where the pot gradient is max

    return round(float(arr))

def pblVPT(startData,saveName):
    hi  = startData[0]
    vpt = startData[3]
    
    vptCutOff = vpt.iloc[0]                                                    #Get VPT ground value as reference
    g = interpolate.UnivariateSpline(hi,vpt-vptCutOff,s=0)                     #generate spline through values above ground value
    
    root_max = []
    g_roots = pd.DataFrame(g.roots())                                          #make dataframe with the roots from the univariate spline
    if len(g_roots) >=1:
        grootVal = int(round(g_roots[0].iloc[-1],3))                           #get last value and round to 3 decimal places
        if grootVal > 3000:                                                    #If over 3Km, higher than where PBL should be and thrown out
            root_max = (grootVal)
            print("     NOTE: VPT Value Exceeding Boundary (3km)")
        else:
            root_max = grootVal
    else:
        root_max = '-'  #If no roots found (often seen with nocturnal layers) NA value
        
    
    vert_ln = [vpt.iloc[1]]*2                                                  #Defines the starting value of VPT as reference
    negXlim = vert_ln[1]-15                                                    #Creates variable for -15 than vertical line VPT 
    posXlim = vert_ln[1]+15    
    return root_max

######################################
#######CONDITIONS FUNCTIONS###########
######################################

def NoctLayer(data):
    depth = 200     #upper depth limit to look for nocturnal layer           
    
    height  = data['Alt']-data['Alt'].iloc[0]    #set ground alt as 0
    upLimit = abs(height-depth).idxmin()         #index location of altitude @ upper depth limit
    temp    = data['T']                          #[C]
    alt     = data['Alt']                        #[m]
    
    t_filt   = pd.Series(temp).rolling(3).mean()  #Rolling mean window=3 - temp
    alt_filt = pd.Series(alt).rolling(3).mean()   #Rolling mean window=3 - alt
    
    t_grad = np.gradient(t_filt,alt_filt)         #Gradient of filtered temp w/r/t altitude
    
    if any(t_grad[0:upLimit] >0):
        noct = 1 #if gradient is present in 0-200m, nocturnal layer = 1 - True
        # print("   Nocturnal Layer Present")
    else:
        noct = 0 #no positive temp gradient = no nocturnal layer = 0 - False
        # print("   --")
    return noct

def lowerStability(startData,data):    
    ######VPT GRADIENT METHOD#########
    depth = 400         #upper depth limit to look for nocturnal layer   

    height = data['Alt']-data['Alt'].iloc[0]        #set ground alt as 0
    upLimit = abs(height-depth).idxmin()            #index location of altitude @ upper depth limit
    dwPt = data['Dewp.']
    alt = data['Alt']
    vpt = startData[3]
    pot = startData[2]
    
    vpt = pd.Series(vpt).rolling(5).mean()          #Rolling mean window=5 - vpt,pot,alt
    pot = pd.Series(pot).rolling(5).mean()
    alt = pd.Series(alt).rolling(5).mean()
    
    grdVPT= np.gradient(vpt.iloc[0:upLimit],alt.iloc[0:upLimit])
    avggrdVPT = np.nanmean(grdVPT)                  #Average the gradient through depth -Negative is unstable
    
    #####BRUNT VIASALA METHOD##########
    g = 9.81
    N2 = ((g/pot)*np.gradient(pot,alt))         #Bruint Vaisala Frequency - N^2 value: negaive would result in imaginary result        
    avgN = np.nanmean(N2.iloc[0:upLimit])       #Average N2 value through depth - negative is unstable
    
    #if VPT and Brunt Viasala both negative: unstable
    if (avgN <0 and avggrdVPT<0):
        stab = 0  #unstable
        # print("  Unstable")
    #If one method negative and one positive: Check values/skew-T
    elif ((avgN <0 and avggrdVPT >0) or (avgN >0 and avggrdVPT<0)):
        stab = 9999 #two methods do not validate - use VPT method
        # print("   Stable-check")
    #If both methods positive: Stable
    else:
        stab = 1    #stable
        # print("   Stable")
    return stab
    
def Hum(data):
    depth = 2000
    
    height   = data['Alt']-data['Alt'].iloc[0] 
    upLimit  = abs(height-depth).idxmin()    
    hum      = data['Hu']
    Hu_avg   = np.mean(hum.iloc[0:upLimit])
    
    if Hu_avg >= 96:    #Sensor has 4% error - any above 96% saturated
        sat = 1         #Fully Saturated (4%Err)
       # print("   Saturated")
    elif Hu_avg >70: 
        sat = 2         #High Saturation (not fully)
        # print("   High Saturation")
    else:
        sat = 0         #Unsaturated
        # print("   Unsaturated")
    return sat
  
def Selection(RunProgram):
    
    if RunProgram[3] == 1:   #Nocturnal Layer  #setting up which values to present from conditions 
        pbl = RunProgram[2]
        method = "PT "
    elif RunProgram[3] !=1 and RunProgram[4] == 1:  #No nocturnal layer, saturated
        pbl = RunProgram[1]
        method = "VPT"
    else:
        pbl = RunProgram[0]   #no nocturnal, no saturation
        method = "RI "
    return pbl,method

########################################
########SAVING FUNCTIONS################
########################################

def fullOutput(datetime,RunProgram,output1,output2,saveName,PBLResults):
    output1.append((saveName,PBLResults[0],PBLResults[1],\
                    ''.join(["Nocturnal Layer" if RunProgram[3] ==1 else "--"]),\
                    ''.join(["Stable" if RunProgram[4] == 1 else "Unstable"]),\
                    ''.join(["Saturated" if RunProgram[5]==1 else "High Saturation" if RunProgram[5]==2 else "Unsaturated"])))
    output2.append((saveName,datetime,RunProgram[0],RunProgram[1],RunProgram[2],PBLResults[1],PBLResults[0]))
    return output1,output2

def printConsole(TotalResults,savePath):
    ########################################################################
    ##########PRINTING NICE OUTPUT FOR ALGORITHUM RESULTS###################
    ########################################################################
    
    #The following is repedative and will not be commented line by line:
        #header is generated and added to lists, {:<20s} parts dictate the position when printing followed by what to put in that position
        #Nocturnal layer precense changes character length and to make clean has different positions
        #Process seems messy however offers CLEAN text file that is simple to understand at a glance
    
    header1 = ['Launch Title', 'PBL [m]','Used Method','Noct Layer','Stability','Saturation']
    results1 = np.array(TotalResults[0])
    results1 = np.insert(results1,[0],header1,axis=0)
    dash1 = '-'*115
    for i in range(len(results1)):
        if i ==0:
            print("\nAlgorithum Results")
            print(dash1)
            print('{:<20s}{:>18s}{:>15s}{:>17s}{:>21s}{:>19s}'.\
                  format(results1[i][0],results1[i][1],results1[i][2],str(results1[i][3]),str(results1[i][4]),results1[i][5]))
            print(dash1)
        else: 
            if results1[i][3] == "Nocturnal Layer":
                print('{:<20s}{:>3}{:>7s}{:>15s}{:>7s}{:>18s}{:>16s}{:>19s}'.\
                      format(results1[i][0],'|',results1[i][1],results1[i][2],'|',results1[i][3],results1[i][4],results1[i][5]))
            else:
                print('{:<20s}{:>3}{:>7s}{:>15s}{:>7s}{:>9s}{:>25s}{:>19s}'.\
                      format(results1[i][0],'|',results1[i][1],results1[i][2],'|',results1[i][3],results1[i][4],results1[i][5]))
    ########################################################################
    ##########PRINTING NICE OUTPUT FOR PBL RESULTS##########################
    ########################################################################
    header2 = ['Launch Title','Launch Time','RI','VPT','PT','Used Method','PBL [m]']
    results2 = np.array(TotalResults[1])
    results2 = np.insert(results2,[0],header2,axis=0)
    dash2 = '-' *135
    for i in range(len(results2)):
        if i == 0:
            print("\n\nPBL Method Results")
            print(dash2)
            print('{:<20s}{:>20s}{:>17s}{:>16s}{:>13s}{:>24s}{:>15s}'.\
                  format(results2[i][0],results2[i][1],results2[i][2],results2[i][3],results2[i][4],results2[i][5],results2[i][6]))
            print(dash2)
        else:
            print('{:<20}{:>23s}{:>3}{:>7}{:>15}{:>14}{:>7}{:>12}{:>17}'.\
                  format(results2[i][0],str(results2[i][1]),'|',results2[i][2],results2[i][3],results2[i][4],'|',results2[i][5],results2[i][6]))
    print("\nProgram Operated On: "+time.strftime("%a, %d %b %Y %H:%M:%S"))
            
def saveTxt(TotalResults,savePath,fileNames):
    ########################################################################
    ##########SAVING CSV AND NICE TEXT FILE FOR ALGORITHUM RESULTS##########
    ########################################################################

    header1 = ['Launch Title', 'PBL [m]','Used Method','Noct Layer','Stability','Saturation']
    results1 = np.array(TotalResults[0])
    results1 = np.insert(results1,[0],header1,axis=0)
    np.savetxt("%s/%s.txt"%(savePath,fileNames[3]),results1,fmt='%s',delimiter=",",encoding="utf-8") #make csv for easy data import if needed, other file looks pretty
    dash1 = '-'*115
    with open('%s/%s.txt'%(savePath,fileNames[1]),'w',encoding='utf-8') as f:
        for i in range(len(results1)):
            if i ==0:
                print("Program Operated On: "+time.strftime("%a, %d %b %Y %H:%M:%S"),file=f)
                print(dash1,file=f)
                print('{:<20s}{:>18s}{:>15s}{:>17s}{:>21s}{:>19s}'.\
                      format(results1[i][0],results1[i][1],results1[i][2],str(results1[i][3]),str(results1[i][4]),results1[i][5]),file=f)
                print(dash1,file=f)
            else: 
                if results1[i][3] == "Nocturnal Layer":
                    print('{:<20s}{:>3}{:>7s}{:>15s}{:>7s}{:>18s}{:>16s}{:>19s}'.\
                          format(results1[i][0],'|',results1[i][1],results1[i][2],'|',results1[i][3],results1[i][4],results1[i][5]),file=f)
                else:
                    print('{:<20s}{:>3}{:>7s}{:>15s}{:>7s}{:>9s}{:>25s}{:>19s}'.\
                          format(results1[i][0],'|',results1[i][1],results1[i][2],'|',results1[i][3],results1[i][4],results1[i][5]),file=f)
       
        
    #########################################################################
    ########SAVING CSV AND NICE TEXT FILE FOR ALL PBL METHOD RESULTS#########
    #########################################################################
    
    header2 = ['Launch Title','Launch Time','RI','VPT','PT','Used Method','PBL [m]']
    results2 = np.array(TotalResults[1])
    results2 = np.insert(results2,[0],header2,axis=0)
    np.savetxt("%s/%s.txt"%(savePath,fileNames[2]),results2,fmt='%s',delimiter=",",encoding="utf-8")
    dash2 = '-' *135
    with open('%s/%s.txt'%(savePath,fileNames[0]),'w',encoding='utf-8')as f:
        for i in range(len(results2)):
           if i == 0:
               print("\n\nPBL Method Results",file=f)
               print(dash2,file=f)
               print('{:<20s}{:>20s}{:>17s}{:>16s}{:>13s}{:>24s}{:>15s}'.\
                     format(results2[i][0],results2[i][1],results2[i][2],results2[i][3],results2[i][4],results2[i][5],results2[i][6]),file=f)
               print(dash2,file=f)
           else:
               print('{:<20}{:>23s}{:>3}{:>7}{:>15}{:>14}{:>7}{:>12}{:>17}'.\
                     format(results2[i][0],str(results2[i][1]),'|',results2[i][2],results2[i][3],results2[i][4],'|',results2[i][5],results2[i][6]),file=f)
        
def mills700(data,millsOutput,saveName):#######################################
      mills = data['Alt'].loc[abs(data['P']-700).idxmin()]
      millsOutput.append((saveName,mills))
      return millsOutput