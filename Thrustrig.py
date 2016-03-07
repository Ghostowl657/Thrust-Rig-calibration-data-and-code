# Thrustrig.py
# Brandon Nadal, (add your name if you work on this)
# Only put active code in here, not functions.

"""Does many things related to the Thrust rig. See the README."""

from math import log,sqrt,e
import matplotlib.pyplot as plt # you need to install this module from command shell
from time import time,clock,ctime,sleep
import serial # the serial module needs to be downloaded
import sys # this might only work on Windows
import numpy as np
from msvcrt import getch # get key press, only Windows
from Thrustrigmodule import * # getting all the functions from the other file


while True: # program will continue to loop until you press CTRL+C
    BAD = False
    takedata = input(' Take data?: ')
    if takedata:
        whatdata = raw_input(' What Data? (FV, MVI): ') # ForceVoltage, MotorVoltageCurrent
        if whatdata == 'FV':
            putSerial("VoltageData.txt")
            V = getVoltageData()
            avV = sum(V)/len(V)
            f = open("CalibrationData.txt",'r')
            a = float(f.readline())
            b = float(f.readline())
            function = f.readline()
            f.close()
            F = a*e**(b*avV)
            print avV
            print F
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
                go = True
                j = getVWData("Thrustdata1.txt"); V1 = j[0]; W1 = j[1]
                j = getVWData("Thrustdata2.txt"); V2 = j[0]; W2 = j[1]
                j = getVWData("Thrustdata3.txt"); V3 = j[0]; W3 = j[1]
                V = V1+V2+V3
                W = W1+W2+W3
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
                    # print '   Data =',len(V) # number of data point used in regression
                    fo = open("CalibrationData.txt",'w')
                    a = str(g[1])
                    b = str(g[2])
                    fo.write(a+'\n')
                    fo.write(b+'\n')
                    fo.write(function)
                    fo.close()
                    # g = g[0]
                    # print g[3]
                    # h = g[3]
                    # k = []
                    # for n in range(len(h)):
                    #     k = k + [abs(h[n])]
                    # print min(k)
                    # print max(k)
                    # print sum(k)/len(k)
                    # PrintStuff('linear',V,g[3])
            elif not calib:
                # input Voltage data and do stuff with it. Like output force, graph, etc.
                V1 = getVoltageData()
                f = open("CalibrationData.txt",'r')
                a = float(f.readline())
                b = float(f.readline())
                function = f.readline()
                f.close()
                x = [0]
                F = []
                #f = open("ForceData.txt",'a')
                if function == 'exponential':
                    for n in range(len(V1)):
                        Fn = a*e**(b*V1[n])
                        F = F + [Fn]
                # for n in range(len(F)-1):
                #     x = x + [x[n]+1]
                #     f.write(str(F[n])+'\n')
                #f.close()
                #MakeWindow(0,max(x),0,max(F))
                #plt.scatter(x,F)
                #MakeWindow(0,max(x),0,max(V1))
                #plt.scatter(x,F)
                MakeWindow(0,5,0,5)
                plt.scatter(V1,F,s=5)
                j = getVWData("Thrustdata1.txt"); V1 = j[0]; W1 = j[1]
                j = getVWData("Thrustdata2.txt"); V2 = j[0]; W2 = j[1]
                j = getVWData("Thrustdata3.txt"); V3 = j[0]; W3 = j[1]
                plt.scatter(V1,W1,c=[1.0,0.0,0.0])
                plt.scatter(V2,W2,c=[0.0,1.0,0.0])
                plt.scatter(V3,W3,c=[1.0,0.0,1.0])
                plt.show()
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
        break
        #print '\n'+' Here we go again!'
