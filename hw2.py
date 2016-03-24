#!/usr/bin/python

# Written by Ryan Hofmann

# Import necessary modules
import sys
import numpy as np
from fread import read

# Check inputs
if len(sys.argv) != 3:
  print "Usage: python hw2.py filename ptype"
  print "ptype = 1,2,3"
  exit()

# Define variables
filename = sys.argv[1]
ptype = int(sys.argv[2])

# Read data into array
time, total, array = read(filename)

# Find first and last elements of type "ptype"
indices = np.where(array==ptype)[0]
try:
  first = indices[0]  
  last = indices[-1]
except IndexError:
  print "No particles of type", ptype
  exit()
N = len(indices)

# Add up all particle masses
mass = np.sum(array[first:last+1], axis=0)[1]/100

# Extract galaxy name from "filename"
end = filename.find('_')
galaxy = filename[0:end]

# Print results
print "The Mass of all particles of Type", ptype, "in Galaxy", galaxy, "is", "%.3f" % mass, "x 10^12 Msun"
print "The total number of particles of Type", ptype, "in Galaxy", galaxy, "is", N
