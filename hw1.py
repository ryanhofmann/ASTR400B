#!/usr/bin/python

# Import necessary modules
import sys
import numpy as np
from fread import read

# Check inputs
if len(sys.argv) != 4:
  print "Usage: python hw1.py filename ptype pnum"
  print "ptype = 1, 2, 3; pnum = integer > 0"
  exit()

# Define variables
filename = str(sys.argv[1])
ptype = int(sys.argv[2])
pnum = int(sys.argv[3])

# Call function to read in data
time, total, array = read(filename)

# Find index of Nth particle
ptype_ind = np.where(array==ptype)[0][0]
p_ind = ptype_ind + (pnum - 1)

# Assign values for Nth particle
m = array[p_ind][1]*1e10
x = array[p_ind][2]
y = array[p_ind][3]
z = array[p_ind][4]
vx = array[p_ind][5]
vy = array[p_ind][6]
vz = array[p_ind][7]

# Compute 3D distance
distance = pow(x**2 + y**2 + z**2, 0.5)

# Compute 3D velocity
velocity = pow(vx**2 + vy**2 + vz**2, 0.5)

# Print answers
print "The 3D Distance of particle", pnum, "of type", ptype, "is :", distance, "kpc"
print "The 3D Velocity of particle", pnum, "of type", ptype, "is :", velocity, "km/s"
print "The Mass of particle", pnum, "of type", ptype, "is :", m, "M_sun"
