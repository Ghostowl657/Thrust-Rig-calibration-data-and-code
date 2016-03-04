# Thrustrigmodule.py
# Brandon Nadal
# Only put functions in here, not active code.

"""This module contains the functions used by Thrustrig.py"""

# Uses formulas from Wolfram Mathworld
# <http://mathworld.wolfram.com/LeastSquaresFitting.html>
# Equations (13), (15)
# <http://mathworld.wolfram.com/LeastSquaresFittingLogarithmic.html>
# Equations (2) and (3)
# <http://mathworld.wolfram.com/LeastSquaresFittingExponential.html>
# Equations (3) and (4)

from math import log,sqrt,e
import matplotlib.pyplot as plt # you need to install this module from the command shell
from time import time,clock,ctime,sleep
import serial # the serial module needs to be downloaded
import sys # this might only work on Windows
from msvcrt import getch # get key press, only Windows


def loadingbar(s,beginT):
    """Displays a loading bar while data is being gathered.
    
    PreC: s is a string
    """
    n = 0
    interval = clock() - beginT
    if interval >= 0.5:
        n = n + 1
        sys.stdout.write('\r'+s+'.'*n) # see note above about sys module
        if len(s) >= 35:
            sys.stdout.write('\r'+s+' '*35)


def putSerial(filename,linelength=6,whatdo='a',serial_port='COM4',baud=9600):
    """[WIP]Interfaces with the Serial port and records the data received in a text file.
    The user can choose which serial port, the baud, the name of the file to save to
    and the length of each line from the serial port. It takes a user input for data cutoff.
    It also displays a loading bar while data is being gathered.
    
    PreC: serial_port is a serial port string (e.g.'COM4'). baud is a int. filename is
    the name string of an existing file. linelength is an int.
    """
    cutoff = raw_input(' Timer, Keypress end, or Number of Data? (T, K, or N): ')
    #with serial.Serial(serial_port,baud) as port, open(filename,whatdo) as fo:
        #init = port.read(size=8
    n = 0; l = 0
    loadT = clock()
    if cutoff == 'T':
        interval = input(' How long in seconds: ')
        beginT = clock()
    elif cutoff == 'N':
        reps = input(' How many data?: ')
    elif cutoff == 'K':
        print '\n'+'Press any key to stop'+'\n'
    else:
        return False
    while True:
        if cutoff == 'T':
            endT = clock()
            elapsedT = endT - beginT
            if elapsedT >= interval:
                break
        elif cutoff == 'N':
            n = n + 1
            if n >= reps:
                break
        elif cutoff == 'K':
            if getch()!=():
                for n in (0,3):
                    sys.stdout.write('\r'+' '*35)
                break
        interval = clock() - loadT
        if interval >= 0.5:
            l = l + 1
            sys.stdout.write('\r'+s+'.'*n)
            if len(s) >= 35:
                sys.stdout.write('\r'+s+' '*35)
        #x = port.read(size=6)
        #fo.writelines(x)
    #fo.close()
    print ' Done'


def rangeData(x0,y0):
    """Takes two input lists and removes the values that don't fall within the range.
    
    PreC: x0 and y0 are equal length lists.
    """
    lowX = input(' Low '+str(x)+': ')
    highX = input(' High '+str(x)+': ')
    y = []; x = []
    for n in range(len(x)):
        if x0[n]<lowX or x0[n]>highX:
            y = y + [y0[n]]
            x = x + [x0[n]]
    return (x,y)


def isfloat(value):
    """Determines if a value is a float
    Output is Boolean
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def islist(value):
    """[WIP] Determines if a value is a list
    Output is Boolean
    """
    try:
        value.insert(0,16)
        return True
    except ValueError:
        return False


def getVWData():
    """Gets Voltage and Weight lists from Thrustdata.txt
    """
    fo = open('Thrustdata.txt', 'r')
    V = []
    W = []
    n = 0
    val = 0
    val_meaning = 'Number'
    # go to the end of the file, record how long it is, then go back to the beginning
    fo.seek(0, 2)
    length = fo.tell()
    fo.seek(0, 0)
    # go through file line by line
    while n != length:
        line = fo.readline(); # reads a line of the file and stores it
        if line == 'V\n':
            val_meaning = 'Voltage'
        elif line == 'W\n':
            val_meaning = 'Weight'
        elif isfloat(line):
            val = float(line)
            if val_meaning == 'Voltage':
                V = V + [val]
            elif val_meaning == 'Weight':
                W = W + [val]
        n = n + 1
    fo.close()
    return (V,W)


def getVoltageData():
    """Stores data in VoltageData.txt as a list.
    See getVWData() for comments.
    """
    fo = open('VoltageData.txt', 'r')
    Vmes = []
    n = 0
    fo.seek(0, 2)
    length = fo.tell()
    fo.seek(0, 0)
    while n != length:
        line = fo.readline(6);
        if isfloat(line) and len(str(line))==6:
            val = float(line)
            Vmes = Vmes + [val]
        n = n + 1
    fo.close()
    return Vmes


def getCapacityData():
    """Takes data in MotorCurrent.txt and MotorVoltage.txt and stores as lists.
    See getVWData() for comments.
    """
    fI = open('MotorCurrent.txt', 'r')
    fV = open('MotorVoltage.txt', 'r')
    I = []
    V = []
    n = 0
    fI.seek(0, 2)
    lengthI = fI.tell()
    fI.seek(0, 0)
    fV.seek(0, 2)
    lengthV = fV.tell()
    fV.seek(0, 0)
    while n != lengthI:
        lineI = fI.readline();
        if isfloat(lineI):
            I = I + [float(lineI)]
    while n != lengthV:
        lineV = fV.readline();
        if isfloat(lineV):
            V = V + [float(lineV)]
        n = n + 1
    fI.close()
    fV.close()
    return (I,V)


def sum_sqrd(x,function='lin'):
    """Finds the sum of x**2 or (lnx)**2.
    
    PreC: x is a list. function is either 'log' or empty.
    """
    x_sum_list = []
    for c in range(len(x)):
        if function == 'log':
            x_sum_list = x_sum_list + [(log(x[c]))**2]
        else:
            x_sum_list = x_sum_list + [(x[c])**2]
    x_sum = sum(x_sum_list)
    return x_sum


def sum_ln(x):
    """Finds the sum of ln(x).
    
    PreC: x is a list.
    """
    lnx = []
    for n in range(len(x)):
        if x[n] > 0:
            lnx = lnx + [log(x[n])]
        else:
            lnx = 0
    ln_sum = sum(lnx)
    return ln_sum


def sum_xy(x,y,function='lin'):
    """Finds the value of a sum of x*y or yln(x).
    
    PreC: x and y are lists. function is either 'log' or empty.
    """
    product = []
    if len(x) <= len(y):
        n = len(x)
    else:
        n = len(y)
    for c in range(n):
        if function == 'log':
            product = product + [log(x[c])*(y[c])]
        else:
            product = product + [(x[c])*(y[c])]
    xy_sum = sum(product)
    return xy_sum


def find_ab(x,y,function):
    """Uses wolfram's equations to calculate a and b.
    
    PreC: x and y are lists, function is 'linear', 'logarithmic', or 'exponential'.
    """
    if function == 'logarithmic':
        xtemp = x
        x = y
        y = xtemp
    
    x_bar = sum(x)/len(x)
    y_bar = sum(y)/len(y)
    x_sqr = sum_sqrd(x)
    xy_sum = sum_xy(x,y)
    if function!='linear':
        ylnx_sum = sum_xy(x,y,'log')
        xlny_sum = sum_xy(y,x,'log')
        lnx_sqr = sum_sqrd(x,'log')
    
    if len(x) <= len(y):
        n = float(len(x))
    else:
        n = float(len(y))
    if function == 'linear':
        a = (y_bar*x_sqr-x_bar*xy_sum)/(x_sqr-n*x_bar**2) # Eq (13)
        b = (xy_sum-n*x_bar*y_bar)/(x_sqr-n*x_bar**2) # Eq (15)
    elif function == 'logarithmic':
        b = (n*ylnx_sum-sum(y)*sum_ln(x))/(n*lnx_sqr-sum_ln(x)**2) # Eq (2)
        a = (sum(y)-b*sum_ln(x))/n # Eq (3)
    elif function == 'exponential':
        A = (sum_ln(y)*x_sqr-sum(x)*xlny_sum)/(n*x_sqr-sum(x)**2) # Eq (3)
        b = (n*xlny_sum-sum(x)*sum_ln(y))/(n*x_sqr-sum(x)**2) # Eq (4)
        a = e**A
    return (a,b)


def MakeWindow(minx,maxx,miny,maxy,labels=True,bgcolor=[1.0,1.0,1.0]):
    """Creates a window with x range minx<=x<=maxx and y range miny<=y<=maxy
    
    If labels is set to False, it will turn off the labeled axes.
    Labeling will not look good if the range is too large, e.g., range>10.
    
    The window will have a background color specified by bgcolor.
    The default is white.
    
    PreC: minx,maxx,miny,maxy are numbers. labels is boolean.
    bgcolor is an RGB list.
    """
    plt.figure(figsize=(8,8), dpi=80)
    # Where to put the axis ticks.
    plt.xticks(np.linspace(int(minx), int(maxx), int(maxx-minx)+1, endpoint=True))
    plt.yticks(np.linspace(int(minx), int(maxy), int(maxy-miny)+1, endpoint=True))
    # The x and y ranges along the axes.
    plt.xlim(int(minx),int(maxx))
    plt.ylim(int(miny),int(maxy))
    # Background color
    axes = plt.gca() #get current axes
    axes.set_axis_bgcolor(bgcolor) 
    if not labels:
        # Suppress the ticks
        axes.set_xticks([]) # remove number labels and ticks
        axes.set_yticks([])


def stats(a,b,x,y,function):
    """Takes values for a and b and calculates the errors.
    
    PreC: a and b are numbers, x and y are lists, function is 'linear',
    'logarithmic', or 'exponential'.
    """
    error = []
    residual = []
    if len(x) <= len(y):
        n = len(x)
    else:
        n = len(y)
    for c in range(n):
        if function == 'linear':
            y_calc = a + b*x[c]
            error = error + [abs((y[c]-y_calc)/y[c])]
            residual = residual + [y[c]-y_calc]
        elif function == 'logarithmic':
            x_calc = a + b*log(y[c])
            error = error + [abs((x[c]-x_calc)/x[c])]
            residual = residual + [x[c]-x_calc]
        elif function == 'exponential':
            y_calc = a*e**(b*x[c])
            error = error + [abs((y[c]-y_calc)/y[c])]
            residual = residual + [y[c]-y_calc]
    av_err = sum(error)/len(error)
    # the following lines are commented out, but plot the residuals of the approximate function
    #
    # if function == 'logarithmic':
    #   x1 = residual
    #   residual = x
    #   x = x1
    # MakeWindow(min(x)-2,max(x)+2,min(y)-2,max(y)+2)
    # plt.scatter(x,y)
    # MakeWindow(min(x)-2,max(x)+2,min(residual)-2,max(residual)+2)
    # plt.plot([0,7],[0,0],linewidth=1,color=[0,0,0])
    # plt.scatter(x,residual)
    # plt.show()
    return (av_err,error,residual)


def PrintStuff(function,V,W):
    """Finds a and b from V and W, tests it, then prints the equation and errors.
    
    PreC: V, W are lists. function is 'linear', 'logarithmic', or 'exponential'
    """
    h = find_ab(V,W,function)
    a = h[0]
    b = h[1]
    g = stats(a,b,V,W,function)
    av_err = g[0]*100
    errormax = max(g[1])
    errormin = min(g[1])
    print '   a =', a
    print '   b =', b
    if function == 'linear':
        print '%6s %1.3f %1s %0.3f %0s' % ('W =',a,'+',b,'* V')
    elif function == 'logarithmic':
        print '%6s %1.3f %1s %1.3f %0s' % ('V =',a,'+',b,'* ln(W)')
    elif function == 'exponential':
        print '%6s %1.3f %0s %0.3f %0s' % ('W =',a,'* e^(',b,'* V)')
    print '%18s %1.5f %0s' % ('Average Error =',av_err,'%')
    print '%14s %1.3f %0s %1.3f %0s' % ('Max error =',errormax*100,
                                    '%, Min error =',errormin*100,'%')
    return (g,a,b)


def capacity(V,I,del_t):
    """[WIP] Takes Voltage, Current, and time interval to
    calculate Power and Energy.
    
    PreC: V,I are both lists or numbers. del_t is a number or list.
    """
    power = []
    total_capacity = []
    for n in range(len(V)):
        power = power + [V[n]*I[n]]
    total_capacity = sum_xy(power,del_t)
    print (total_capacity,power)
