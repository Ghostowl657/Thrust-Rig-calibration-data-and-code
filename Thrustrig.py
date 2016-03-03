# Thrustrig.py
# Brandon Nadal
# 2/29/16

"""Takes data points from the thrust rig and calculates, using least
 squares regression analysis, and calculates the function [V=a+b*W] or
 [V=a+bln(W)]"""

# Uses formulas from Wolfram Mathworld
# <http://mathworld.wolfram.com/LeastSquaresFitting.html>
# Equations (13), (15)
# <http://mathworld.wolfram.com/LeastSquaresFittingLogarithmic.html>
# Equations (2) and (3)
# <http://mathworld.wolfram.com/LeastSquaresFittingExponential.html>
# Equations (3) and (4)

from math import log,sqrt,e
from time import time,sleep

# Weight of test 1
W1 = [2.024,2.516,3.084,3.64,4.36,4.918,5.616,6.25,
      6.972,7.694,8.234,8.874] # removed 0.254,0.56,0.884,1.188,1.532 outliers
# Voltage of test 1
V1 = [4.0,4.2,4.33,4.47,4.57,4.62,4.69,4.74,4.78,
      4.82,4.85,4.87] # removed 1.9,2.49,2.79,3.32,3.8 outliers
# Weight of test 2
W2 = [1.532,2.024,2.516,3.214,3.934,4.656,5.376,5.944,6.484,
      7.042,7.598,8.238,8.872] # removed 0.254 outlier
# Voltage of test 2
V2 = [3.9,4.07,4.22,4.36,4.49,4.6,4.67,4.72,4.78,
      4.8,4.81,4.83,4.86] # removed 1.9 outlier
# Weight of test 3
W3 = [6.292,6.78,7.272,7.992,8.712,9.114,9.416,10.008,
      10.384,10.704,11.024] # removed 1.28 outlier
# Voltage of test 3
V3 = [4.77,4.79,4.82,4.85,4.88,4.92,4.93,4.93,4.94,
      4.94,4.95] # removed 3.635 outlier
# Weight of test 4
W4 = [1.28,6.292,6.612,7.206,7.926,8.33,8.65,9.37,9.862,
      10.35,10.654,10.97]
# Voltage of test 4
V4 = [4.22,4.775,4.8,4.825,4.85,4.87,4.89,4.905,4.92,
      4.935,4.94,4.95]
# Weight of test 5
W5 = [1.28,6.292,7.012,7.732,8.048,8.352,8.672,8.992,9.396,
      9.888,10.376,10.97]
# Voltage of test 5
V5 = [4.22,4.775,4.8,4.85,4.86,4.87,4.88,4.89,4.9,4.91,
      4.925,4.945]

def isfloat(value):
  """Determines if a value is a float
  Output is Boolean
  """
  try:
    float(value)
    return True
  except ValueError:
    return False

"""# Getting Voltage and Weight lists from a data text file
fo = open('Thrustdata.txt', 'r')
V = []
W = []
n = 0
position = 0
val = 0
val_meaning = 'Number'
fo.seek(0, 2)
length = fo.tell()
fo.seek(0, 0)
while n != length:
    line = fo.readline();
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
fo.close()"""

# Concatenating
W = W1+W2+W3+W4+W5
V = V1+V2+V3+V4+V5


def sum_sqrd(x,function='lin'):
    """Finds the sum of x**2 or (lnx)**2.
    x is a list. function is either 'log' or empty.
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
    """Finds the sum of ln(x). x is a list.
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
    x and y are lists. function is either 'log' or empty.
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
    x and y are lists, function is 'linear', 'logarithmic', or 'exponential'.
    """
    if function == 'logarithmic':
        xtemp = x
        x = y
        y = xtemp
    
    x_bar = sum(x)/len(x)
    y_bar = sum(y)/len(y)
    x_sqr = sum_sqrd(x)
    xy_sum = sum_xy(x,y)
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


def test_ab(a,b,x,y,function,d=0):
    """Takes values for a and b and calculates the errors.
    a and b are numbers, x and y are lists, function is 'linear', 'logarithmic', or 'exponential'.
    """
    error = []
    if len(x) <= len(y):
        n = len(x)
    else:
        n = len(y)
    for c in range(n):
        if function == 'linear':
            y_calc = a + b*x[c]
            error = error + [abs((y[c]-y_calc)/y[c])]
        elif function == 'logarithmic':
            x_calc = a + b*log(y[c])
            error = error + [abs((x[c]-x_calc)/x[c])]
        elif function == 'exponential':
            y_calc = a*e**(b*x[c])+d
            error = error + [abs((y[c]-y_calc)/y[c])]
    av_err = sum(error)/len(error)
    return (av_err,error)


def PrintStuff(function,V,W):
    """Finds a and b from V and W, tests it, then prints the equation and errors.
    V, W are lists. function is 'linear', 'logarithmic', or 'exponential'
    """
    h = find_ab(V,W,function)
    a = h[0]
    b = h[1]
    g = test_ab(a,b,V,W,function)
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
    return g


if __name__ == '__main__':
    choice = str(raw_input(' Linear, Logarithmic, or Exponentional approximation?: '))
    rang = input(' Weight range? (True/False): ')
    if rang:
        lowW = input(' Low W: ')
        highW = input(' High W: ')
        r = len(W)
        W0 = W
        V0 = V
        W = []
        V = []
        n = 0
        while n < len(W0):
            if W0[n] >= lowW and W0[n] <= highW: # making new lists for W and V with all lists within the range
                W = W + [W0[n]]
                V = V + [V0[n]]
            n = n + 1
    if ('lin' in choice or 'Lin' in choice):
        function = 'linear'
        go = True
    elif ('log' in choice or 'Log' in choice or choice == 'ln'):
        function = 'logarithmic'
        go = True
    elif ('exp' in choice or 'Exp' in choice or choice == 'e'):
        function = 'exponential'
        go = True
    else:
        print 'Sorry bad input, try again.'
        go = False
    if go:
        g = PrintStuff(function,V,W)
        print '   Data =',len(V)
        # print g[1]
        
        """delt_err = -1
        d = 0
        err_mem = []
        while delt_err < 0 and function == 'exponential':
            st_err = g[1]
            d = d - 10**(-6)
            h = find_ab(V,W,function)
            g = test_ab(h[0],h[1],V,W,function,d)
            en_err = g[1]
            delt_err = sum(en_err)/len(en_err)-sum(st_err)/len(st_err)
            err_mem = err_mem + [delt_err]
        else:
            if function == 'exponential':
                err_mem = sum(err_mem)/len(err_mem)
                print d, delt_err, err_mem
                PrintStuff(function,V,W)"""
        
        """redo = input('Make it more accurate?: ')
        while redo == True:
            accuracy = input('How accurate?: ')
            Vacc = []
            Wacc = []
            err = g[1]
            for n in range(len(V)):
                if err[n] < accuracy:
                    Vacc = Vacc + [V[n]]
                    Wacc = Wacc + [W[n]]
            if len(Vacc) == 0:
                quit()
            PrintStuff(function,Vacc,Wacc)
            print '   Data=',len(Vacc)
            redo = input('Make it more accurate?: ')"""