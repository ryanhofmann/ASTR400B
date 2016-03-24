#!/usr/bin/python

# Written by Ryan Hofmann

import sys
import numpy as np
import matplotlib.pyplot as plt
from v_r import v_r

# Check inputs
if len(sys.argv) != 4:
  print "Usage: python v_plot.py galaxy snap rmax"
  print "0 <= snap <= 999"
  exit()

# Assign variables
galaxy = sys.argv[1]
snap = sys.argv[2]
rmax = float(sys.argv[3])
fin = galaxy+'_'+snap.zfill(3)+'.txt'

# Compute rotation curve for each component
r, M1, v1 = v_r(galaxy, 1, snap, rmax)
r, M2, v2 = v_r(galaxy, 2, snap, rmax)
#r, M3, v3 = v_r(galaxy, 3, snap, rmax)

# Compute total rotation curve
G = 4.30e-6 # [kpc/Msun]*[km/s]^2
M = M1 + M2 #+ M3
v = np.sqrt(G*M*1e10/(r + 1e-10))

# Plot rotation curves
plt.plot(r, v1, 'ko', label='dark matter')
plt.plot(r, v2, 'b*', markersize=8, label='disk')
#plt.plot(r, v3, 'r*', markersize=8, label='bulge')
plt.plot(r, v, 'y-', linewidth=3, label='total')
plt.xlabel('r [kpc]')
plt.ylabel('v(r) [km/s]')
plt.title('Rotation curves')
plt.legend(ncol=2)
#plt.ylim(0, 260)
plt.show()
