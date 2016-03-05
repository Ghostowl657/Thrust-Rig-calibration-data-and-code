# Trustrigmodule.py
Contains the functions that thrustrig uses

# Thrustrig.py
Main code:

What it does:
1. It can find the least squares approximation for linear, logarithmic, or exponential (probably add more) regression from a set of data, depending on user input.
  - We'll use it to find the function Force(Voltage) for our force sensor.
  - More statistical data are coming soon [WIP]
  - The sets of data are known weights (force) and measured Voltage.
2. It can interface with the serial port and record the Voltage data coming from the Arduino (port=COM4, baud=9600).
  - The user can select three ways of limiting the data gathered:
      i. By having it run on a timer, and specifying how long to run before ending the gathering process (e.g. 5 seconds)
      ii. By having it only gather a specific amount of data (e.g. 750 entries)
      iii. By having it run until a keypress
3. It can take a text file and read it to get data, to be used in the code.
  - We can input Voltage data from the force sensor and output Force (i.e. thrust) by running it through the function found in (1).
  - [WIP] We can input Voltage and Current data from the motor (and optionally time data), to output Power and Total Energy(i.e. battery capacity).
4. [WIP] More coming
  - Real time graphing?
  - Translate to MATLAB?
  - Optimize


How to use:
 Windows:
 1. Have activepython and the necessary modules
 2. Change directory with cd command (e.g. cd desktop/code) to wherever the file is saved
 3. Run command "python Thrustrig.py"
 4. Answer "Take Data?:" with "True" or "False" (case sensitive)
 5. Answer "What Data?:" with "FV" for force sensor (ForceVoltage) or "MVI" for motor measurments (MotorVoltageCurrent)
 6. Answer "Force, Capacity: " with "Force" or "Capacity"
 7. Answer "Calibration?:" with "True" or "False"
 8. The answer for "Linear, Logarithmic..." can be anything that makes sense
 9. Answer "Weight range?" with "True" or "False"
 10. Have fun <-- This is a requirement. If you do not do this, the output will be corrupted.
