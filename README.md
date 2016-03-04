# Thrusting.py
Thrusting code:

What it does:
1. It can find the least squares approximation for linear, logarithmic, or exponential (probably add more) regression from a set of data, depending on user input.
  - We'll use it to find the function Force(Voltage) for our force sensor.
  - More statistical data are coming soon [WIP]
  - The sets of data are known weights (force) and measured Voltage.
2. It can interface with the serial port and record the Voltage data coming from the Arduino (port=COM4, baud=9600).
  - The user can select three ways of limiting the data gathered:
      i. By having it run on a timer, and specifying how long to run before ending the gathering process (e.g. 5 seconds)
      ii. By having it only gather a specific amount of data (e.g. 750 entries)
      iii. 
3. It can take a text file and read it to get data, to be used in the code.
  - We can input Voltage data from the force sensor and output Force (i.e. thrust) by running it through the function found in (1).
  - [WIP] We can input Voltage and Current data from the motor (and optionally time data), to output Power and Total Energy(i.e. battery capacity).
4. [WIP] More coming
  - Real time graphing?
  - Translate to MATLAB?
  - Make it more efficient


How to use:
[WIP]
