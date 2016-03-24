#!/usr/bin/python

# Written by Ryan Hofmann

# Import necessary modules
import sys
import numpy as np
from fread import read
from COM import COM

# Check inputs
if len(sys.argv) != 5:
  print "Usage: python hw4.py galaxy ptype min max"
  print "galaxy = MW,M31,M33; ptype = 1,2,3; 0 <= min < max"
  exit()

# Define variables
galaxy = sys.argv[1]
ptype = int(sys.argv[2])
tmin = int(sys.argv[3])
tmax = int(sys.argv[4])

# Open file for writing
fout = 'COM_' + galaxy + '.txt'
print fout
f = open(fout, 'w')
f.write('#time\txcom\tycom\tzcom\tvxcom\tvycom\tvzcom\n')

# For each snap, find xcom and vcom
for i in range(tmin,tmax+1):

  # Generate filenames
  number = str(999000 + i)
  number = number.split('999')[-1]
  fin = galaxy + '_' + number + '.txt'
  print fin

  # Find COM position and velocity
  time, com, vcom = COM(fin, ptype)
  print time, com, vcom

  # Write results to file
  t = str(time)
  x = '%s' % float('%.3g' % com[0])
  y = '%s' % float('%.3g' % com[1])
  z = '%s' % float('%.3g' % com[2])
  vx = '%s' % float('%.3g' % vcom[0])
  vy = '%s' % float('%.3g' % vcom[1])
  vz = '%s' % float('%.3g' % vcom[2])
  string = t+'\t'+x+'\t'+y+'\t'+z+'\t'+vx+'\t'+vy+'\t'+vz+'\n'
  f.write(string)

# Close file
f.close()
