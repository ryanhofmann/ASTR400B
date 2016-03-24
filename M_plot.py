#!/usr/bin/python

# Written by Ryan Hofmann

import sys
import matplotlib.pyplot as plt
from M_r import M_r

# Check inputs
if len(sys.argv) != 5:
  print "Usage: python M_plot.py galaxy ptype snap rmax"
  print "ptype = 1,2,3; 0 <= snap <= 0; rmax in kpc"
  exit()

# Define variables
galaxy = sys.argv[1]
ptype = int(sys.argv[2])
snap = sys.argv[3]
rmax = int(sys.argv[4])

# Calculate M(r)
r, m = M_r(galaxy, ptype, snap, rmax)

# Plot M(r) vs r
M = 197.
a = 106.
plt.plot(r, m, 'bo')
plt.plot(r, M*(1 - a*(2*r + a)/(r + a)**2), 'b--')
plt.xlabel('r (kpc)')
plt.ylabel('M(r) (10^10 Msun)')
plt.show()
