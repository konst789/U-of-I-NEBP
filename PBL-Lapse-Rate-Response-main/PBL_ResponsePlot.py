# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 16:12:46 2021

This program contains plotting functions to plot the PBL response using the following methods:
    -PT
    -RI
    -VPT
    -Algorithm

This propgram operates off of data created by the saved csv file created 
from the PBL algorithm program. 

***TO OPERATE, CHANGE LINE 29 TO THE FILE PATH OF THE GENERATED "PBLMethodsCSV_XXX.txt"
   that was saved durring operation of last program - if "save" was chosen***
   
This program was initially created for reference purposes only and has since been adjusted 
to operate in tandem with the PBL algorithm associated with Alex Chambers PBL development program.
Multiple plotting operations are available and may be utilized, however "scatter" is the primary
plotting method used in associated publication. 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime

algFile = r"C:\Users\scba228\Dropbox\RESEARCH\NEBP\Workshop\Data Analysis with Python\Sample Data Output\PBLMethodsCSV_Tolten.txt"
algdf = pd.read_csv(algFile,na_values="-",parse_dates=[1]) 

pblData = algdf[['RI','VPT','PT','PBL [m]']].copy()
pblData.rename(columns={'PBL [m]':"algorithm"},inplace=True)
date = algdf['Launch Time']


pblData = pblData.set_index(algdf['Launch Time'])

day1 = datetime(2020,12,14,00,00,00)
day2 = datetime(2020,12,15,00,00,00)
totality = datetime(2020,12,14,16,13,28,00)
first_contact = datetime(2020,12,14,15,00,00)
last_contact  = datetime(2020,12,14,17,30,00)

def plotLines(pblData,day1,day2,totality,first_contact,last_contact):
    n=1
    fig,ax = plt.subplots(figsize=(8,6))
    plt.plot(pblData.index,pblData['RI'],label='RI')
    plt.plot(pblData.index,pblData['VPT'],label='VPT')
    plt.plot(pblData.index,pblData['PT'],label='PT')
    plt.plot(pblData.index,pblData['algorithm'],label='algorithm')
    
    upper = plt.ylim()[1]+50
    ax.vlines(totality,0,upper,colors='red')
    ax.axvspan(first_contact,last_contact,color='green',alpha=0.3)
    ax.legend()
    
    #plt.title("Calculated PBL Heights for Eclipse Campaign",size=15,weight='bold')
    plt.ylabel("Altitude AGL [m]",size=12,weight='bold')
    plt.xlabel("Launch Time [UTC]",size=12,weight='bold')
    ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    plt.xticks(pblData.index,rotation=90)
    [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
    plt.show()

def plotLinesMarker(pblData,day1,day2,totality,first_contact,last_contact):
    n=1
    fig,ax = plt.subplots(figsize=(8,6))
    plt.plot(pblData.index,pblData['RI'],alpha=.5,marker='+',label='RI')
    plt.plot(pblData.index,pblData['VPT'],alpha=.5,marker='p',label='VPT')
    plt.plot(pblData.index,pblData['PT'],alpha=.5,marker='s',label='PT')
    plt.plot(pblData.index,pblData['algorithm'],alpha=.5,marker='P',label='algorithm')
    
    upper = plt.ylim()[1]+50
    ax.vlines(totality,0,upper,colors='red')
    ax.axvspan(first_contact,last_contact,color='green',alpha=0.3)
    ax.legend()
    
    #plt.title("Calculated PBL Heights for Eclipse Campaign")
    plt.ylabel("Altitude AGL [m]")
    plt.xlabel("Launch Time [UTC]")
    ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    plt.xticks(pblData.index,rotation=90)
    [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
    plt.show()
  
    
def plotScatter(pblData,day1,day2,totality,first_contact,last_contact):
    n=1
    fig,ax = plt.subplots(figsize=(8,6))
    plt.scatter(pblData.index,pblData['RI'],marker='+',label='RI')
    plt.scatter(pblData.index,pblData['VPT'],marker='p',label='VPT')
    plt.scatter(pblData.index,pblData['PT'],marker='s',label='PT')
    plt.plot(pblData.index,pblData['algorithm'],color='black',label='Algorithm')
    
    upper = plt.ylim()[1]+50
    ax.vlines(totality,0,upper,colors='red',linewidth=1)
    ax.axvspan(first_contact,last_contact,color='green',alpha=0.3)
    ax.legend()
    
    plt.title("Calculated PBL Heights for Eclipse Campaign",size=18,weight='bold')
    plt.ylabel("Altitude AGL (m)",size=15)
    plt.xlabel("Launch Time (UTC)",size=15)
    ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    plt.xticks(pblData.index,rotation=90,size=6)
    [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
    # plt.savefig("C:/Users/alex/OneDrive - University of Idaho/ISGC/Publication/Figures/Publication Images/PBLResponse_M(3.25).tiff",dpi=300)
    plt.show()

def plotAlg(pblData,day1,day2,totality,first_contact,last_contact):
    n=1
    fig,ax = plt.subplots(figsize=(8,6))
    plt.plot(pblData.index,pblData['algorithm'],label='Algorithm',marker='d')
    
    upper = plt.ylim()[1]+50
    ax.vlines(totality,0,upper,colors='red')
    ax.axvspan(first_contact,last_contact,color='green',alpha=0.3)
    ax.legend()
    
    plt.title("Algorithm PBL Heights for Eclipse Campaign",size=18,weight='bold')
    plt.ylabel("Altitude AGL [m]",size=12,weight='bold')
    plt.xlabel("Launch Time [UTC]",size=12,weight='bold')
    ax.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
    plt.xticks(pblData.index,rotation=90,size=8)
    [l.set_visible(False) for (i,l) in enumerate(ax.xaxis.get_ticklabels()) if i % n != 0]
    # plt.savefig("HighRes_Alg.jpg",dpi=3000)
    plt.show()

    
# plotLines(pblData,day1,day2,totality,first_contact,last_contact)
# plotLinesMarker(pblData,day1,day2,totality,first_contact,last_contact)
# plotAlg(pblData,day1,day2,totality,first_contact,last_contact)

plotScatter(pblData,day1,day2,totality,first_contact,last_contact)
