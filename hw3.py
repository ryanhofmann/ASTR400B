#!/usr/bin/python

# Written by Ryan Hofmann

# Import necessary modules
import sys
import numpy as np
from fread import read
from COM import COM

# Check inputs
if len(sys.argv) != 3 and len(sys.argv) != 4:
  print "Usage: python hw3.py filename ptype [tol=2]"
  print "ptype = 1, 2, 3; pnum = integer > 0"
  exit()

# Define variables
fname = sys.argv[1]
ptype = int(sys.argv[2])
tol = 2
if len(sys.argv) == 4:
  tol = float(sys.argv[3])

# Execute function
time, com, vcom = COM(fname, ptype, tol)

# Print results
np.set_printoptions(suppress=True)
print time, com, vcom
