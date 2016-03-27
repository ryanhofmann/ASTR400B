#!/usr/bin/python

# Written by Ryan Hofmann

# Define plotting function
def disk_plot(galaxy, snap, plane='xy'):

  # Import necessary modules
  import numpy as np
  import matplotlib.pyplot as plt
  from fread import read
  from COMread import COMread

  # Construct file name
  number = str(999000 + snap)
  number = number.split('999')[-1]
  fname = galaxy+'_'+number+'.txt'

  # Read in data
  time, total, data = read(fname)
  ind = np.where(data == 2)[0]
  data = data[ind]

  # Read in COM data
  time, com, vcom = COMread(galaxy)

  # Extract disk positions in specified plane
  if plane == 'xy':
    x1 = data[:,2]
    x2 = data[:,3]
    x1com = com[:,0]
    x2com = com[:,1]
  if plane == 'xz':
    x1 = data[:,2]
    x2 = data[:,4]
    x1com = com[:,0]
    x2com = com[:,2]
  if plane == 'yz':
    x1 = data[:,3]
    x2 = data[:,4]
    x1com = com[:,1]
    x2com = com[:,2]

  # Determine plot limits
  xbuffer = 0.1*(np.max(x1) - np.min(x1))
  ybuffer = 0.1*(np.max(x2) - np.min(x2))
  xmin = np.min(x1) - xbuffer
  xmax = np.max(x1) + xbuffer
  ymin = np.min(x2) - ybuffer
  ymax = np.max(x2) + ybuffer

  # Plot disk particles
  from matplotlib.colors import LogNorm
  plt.hist2d(x1, x2, bins=60, norm=LogNorm())
  plt.plot(x1com, x2com, 'r')
#  plt.axis([xmin,xmax,ymin,ymax])
  plt.xlabel('kpc')
  plt.ylabel('kpc')
  plt.gca().set_aspect('equal', adjustable='box')
  plt.colorbar()
  plt.show()

# Execute function
if __name__ == '__main__':
  # Import necessary modules
  import numpy as np
  import sys

  # Check inputs
  if len(sys.argv) != 4:
    print "Usage: python disk_plot.py galaxy snap plane"
    print "plane = xy,xz,yz"
    exit()

  # Assign variables
  galaxy = sys.argv[1]
  snap = int(sys.argv[2])
  plane = sys.argv[3]

  # Run function
  disk_plot(galaxy, snap, plane)
