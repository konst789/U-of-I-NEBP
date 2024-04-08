# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 11:11:34 2023
@author: Logan Kearney
Version: 1.0
Last Updated: 9/28/2023
"""

#Dependencies
from colorama import Fore, Back, Style

def OutputFormatReference():
    print('\n')
    print(Style.BRIGHT + Fore.WHITE + Back.RESET + "General Message - White")
    print(Style.BRIGHT +Fore.GREEN + Back.RESET + "Success Message - Green")
    print(Style.BRIGHT + Fore.WHITE + Back.GREEN + "Critical Success Message - White on Green")
    print(Style.BRIGHT +Fore.YELLOW + Back.RESET + "Warning Message - Yellow")
    print(Style.BRIGHT +Fore.RED + Back.RESET + "Error Message - Red")
    print(Style.BRIGHT +Back.RED + Fore.WHITE + "Critical Error Message - White on Red")
    print(Style.BRIGHT +Fore.MAGENTA + Back.RESET + "Special Info Message - Magenta")
    print(Style.BRIGHT + Fore.CYAN + Back.RESET + "Program Info Message - Cyan")

def txt (Message,DoPrint):
    #Default Text Message
    Message = str(Message)
    if (DoPrint == True):
        print(Style.BRIGHT + Fore.WHITE + Back.RESET + Message)
    else:
        pass

def wrn (Message,DoPrint):
    #Warning Message
    Message = str(Message)
    if (DoPrint == True):
        print(Style.BRIGHT + Fore.YELLOW + Back.RESET + Message)
    else:
        pass

def err (Message,DoPrint):
    #Error Message
    Message = str(Message)
    if (DoPrint == True):
        print(Style.BRIGHT + Fore.RED + Back.RESET + Message)
    else:
        pass

def cem (Message,DoPrint):
    #Critical Error Message
    Message = str(Message)
    if (DoPrint == True):
        print(Style.BRIGHT + Fore.WHITE + Back.RED + Message)
    else:
        pass

def scs (Message,DoPrint):
    #Success Message
    Message = str(Message)
    if (DoPrint == True):
        print(Style.BRIGHT + Fore.GREEN + Back.RESET + Message)
    else:
        pass

def csm (Message,DoPrint):
    #Critical Success Message
    Message = str(Message)
    if (DoPrint == True):
        print(Style.BRIGHT + Fore.WHITE + Back.GREEN + Message)
    else:
        pass

def sim (Message,DoPrint):
    #Special Info Message
    Message = str(Message)
    if (DoPrint == True):
        print(Style.BRIGHT + Fore.MAGENTA + Back.RESET + Message)
    else:
        pass

def pim (Message,DoPrint):
    #Program Info Message
    Message = str(Message)
    if (DoPrint == True):
        print(Style.BRIGHT + Fore.CYAN + Back.RESET + Message)
    else:
        pass

def OutputTest():
    print('\n')
    txt('Message Test',True)
    wrn('Warning Message Test',True)
    err('Error Message Test',True)
    cem('Critical Error Message Test',True)
    sim('Special Info Message Test',True)
    pim('Program Info Message Test',True)
    scs('Success Message Test',True)
    csm('Critical Success Message Test',True)
    pim('Output Test Complete!',True)
    print('\n')