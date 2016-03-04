# Thrustrig.py
# Brandon Nadal, (add your name if you work on this)
# Only put active code in here, not functions.

"""Does many things related to the Thrust rig. See the README."""

from math import log,sqrt,e
import matplotlib.pyplot as plt # you need to install this module from command shell
from time import time,clock,ctime,sleep
import serial # the serial module needs to be downloaded
import sys # this might only work on Windows
from msvcrt import getch # get key press, only Windows
from Thrustrigmodule import * # getting all the functions from the other file


while True: # program will continue to loop until you press CTRL+C
    BAD = False
    takedata = input(' Take data?: ')
    if takedata:
        whatdata = raw_input(' What Data? (FV, MVI): ') # ForceVoltage, MotorVoltageCurrent
        if whatdata == 'FV':
            putSerial("VoltageData.txt")
        elif whatdata == 'MVI':
            pass
        else:
            BAD = True
    elif not takedata:
        whatdo = raw_input(' Force, Capacity: ')
        if whatdo == 'Force': # Using force sensor
            calib = input(' Calibration?: ')
            # Finding the function of force to voltage through least squares approximation
            if calib:
                choice = raw_input(' Linear, Logarithmic, or Exponentional approximation?: ')
                j = getVWData(); V = j[0]; W = j[1]; go = True
                if ('lin' in choice or 'Lin' in choice):
                    function = 'linear'
                elif ('log' in choice or 'Log' in choice or choice == 'ln' or choice == 'Ln'):
                    function = 'logarithmic'
                elif ('exp' in choice or 'Exp' in choice or choice == 'e' or choice == 'E'):
                    function = 'exponential'
                else:
                    go = False; BAD = True
                if go:
                    if input(' Weight range? (True/False): '):
                        newVW = rangeData(V,W)
                        V = newVW[0]; W = newVW[1]
                    g = PrintStuff(function,V,W)
                    print '   Data =',len(V) # number of data point used in regression
            elif not calib:
                # input Voltage data and do stuff with it. Like output force, graph, etc.
                pass
        elif whatdo == 'Capacity':
            j = getCapacityData()
            I = j[0]
            V = j[1]
            pass
        else:
            BAD = True
    else:
        BAD = True
    if BAD:
        print ' Sorry, bad input. Try again.'
    else:
        print '\n'+' Here we go again!'
