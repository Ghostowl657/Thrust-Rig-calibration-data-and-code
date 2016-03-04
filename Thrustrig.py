# Thrustrig.py
# Brandon Nadal, (add your name if you work on this)

"""Does many things related to the Thrust rig. See the README."""

# Uses formulas from Wolfram Mathworld
# <http://mathworld.wolfram.com/LeastSquaresFitting.html>
# Equations (13), (15)
# <http://mathworld.wolfram.com/LeastSquaresFittingLogarithmic.html>
# Equations (2) and (3)
# <http://mathworld.wolfram.com/LeastSquaresFittingExponential.html>
# Equations (3) and (4)

from math import log,sqrt,e
import matplotlib.pyplot as plt # you need to install this module from command shell
from time import time,clock,ctime
import serial # the serial module needs to be downloaded
import sys # this might only work on Windows


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
    lengthI = fo.tell()
    fI.seek(0, 0)
    fV.seek(0, 2)
    lengthV = fo.tell()
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


if __name__ == '__main__':
    while True: # program will continue to loop until you press CTRL+C
        BAD = False
        takedata = input(' Take data?: ')
        if takedata:
            reps_or_naw = raw_input(' Timer, Keypress end, or Number of Data? (T, K, or N): ')
            with serial.Serial('COM4',9600) as port, open('VoltageData.txt','a') as outf:
                if reps_or_naw == 'T':
                    interval = input(' How long in seconds: ')
                    begindotT = clock()
                    elapsedT = 0
                    while elapsedT <= interval:
                        dotT = clock() - begindotT
                        if dotT >= 0.5: # this makes a loading bar of sorts
                            dotdot = dotdot + '.'
                            sys.stdout.write('\r'+dotdot) # sys might be Windows only
                            if len(dotdot) >= 35:
                                dotdot = ' Gathering Data.'
                                sys.stdout.write('\r'+' Gathering Data.'+' '*25)
                            begindotT = clock()
                        x = port.read(size=6) # reads a line (e.g. 0.1932)
                        outf.writelines(x) # and writes it to VoltageData.txt
                        endT = clock()
                        elapsedT = endT - beginT
                elif reps_or_naw == 'N':
                    reps = input(' How many data?: ')
                    init = port.read(size=8)
                    for n in range(reps):
                        x = port.read(size=6)
                        outf.writelines(x)
                elif reps_or_naw == 'K':
                    cont = True
                    beginT = clock() - 1.5
                    print ' '
                    print ' Press any key to stop' # this doesn't happen yet...
                    print ' '
                    dotdot = ' Gathering Data'
                    while cont:
                        interval = clock() - beginT
                        if interval >= 0.5: # this makes a loading bar of sorts
                            dotdot = dotdot + '.'
                            sys.stdout.write('\r'+dotdot) # see note above about sys
                            if len(dotdot) >= 35:
                                dotdot = ' Gathering Data.'
                                sys.stdout.write('\r'+' Gathering Data.'+' '*25)
                            beginT = clock()
                        x = port.read(size=6) # reads a line (e.g. 0.1932)
                        outf.writelines(x) # and writes it to VoltageData.txt
                sleep(0.25)
                outf.close()
        elif not takedata:
            whatdo = raw_input(' Force, Capacity: ')
            if whatdo == 'Force': # Using force sensor
                calib = input(' Calibration?: ')
                # Finding the function of force to voltage through least squares approximation
                if calib:
                    choice = raw_input(' Linear, Logarithmic, or Exponentional approximation?: ')
                    j = getVWData()
                    V = j[0]
                    W = j[1]
                    go = True
                    if ('lin' in choice or 'Lin' in choice):
                        function = 'linear'
                    elif ('log' in choice or 'Log' in choice or choice == 'ln' or choice == 'Ln'):
                        function = 'logarithmic'
                    elif ('exp' in choice or 'Exp' in choice or choice == 'e' or choice == 'E'):
                        function = 'exponential'
                    else:
                        go = False
                        BAD = True
                    if go:
                        rang = input(' Weight range? (True/False): ')
                        if rang:
                            lowW = input(' Low W: ')
                            highW = input(' High W: ')
                            r = len(W)
                            W0 = W # temporary storage
                            V0 = V # ""             ""
                            W = []
                            V = []
                            n = 0
                            while n < len(W0):
                                # making new lists for W and V with all lists within the range
                                if W0[n] >= lowW and W0[n] <= highW:
                                    W = W + [W0[n]]
                                    V = V + [V0[n]]
                                n = n + 1
                        g = PrintStuff(function,V,W)
                        print '   Data =',len(V) # number of data point used in regression
                elif not calib:
                    # input Voltage data and do stuff with it. Like output force, graph, etc.
                    pass
            elif whatdo == 'Capacity':
                j = getCapacityStuff()
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
            print ' Here we go again!'