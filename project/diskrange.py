#!/usr/bin/python

# Written by Ryan Hofmann

from functions import read
from functions import COM
import numpy as np
import matplotlib.pyplot as plt
from disk import AngMomShift

# Define function for plotting disk over range of snaps
def DiskRange(galaxy, first, last, rmax=50, axes='xy'):

  print galaxy, first, last, axes

  # Create subfolder in which to place images
  firststr, laststr = '%03d' % first, '%03d' % last
  if '/' in galaxy:
    fgalaxy = galaxy.split('/')[-1]
  else:
    fgalaxy = galaxy
  dirname = fgalaxy + '_' + firststr + '_' + laststr + '_' + axes
  print dirname
  import os
  if not os.path.isdir(dirname):
    os.makedirs(dirname)

  # Loop over snap range
  i = 0
  for snap in range(first, last+1):

    # Construct file name
    snapstr = '%03d' % snap
    infile = galaxy + '_' + snapstr + '.txt'
    print infile

    # Read in data from file
    time, total, data = read(infile)

    # Compute COM and shift to COM frame
    time, com, vcom = COM(infile, 3, tol=0.5)
    pos = data[:, 2:5] - com
    vel = data[:, 5:8] - vcom

    # Select region for plotting
    rmax = 50
    r = np.sqrt(np.sum(np.square(pos), axis=1))
    pos = pos[np.where(r < rmax and data == 2)[0]]
    vel = vel[np.where(r < rmax and data == 3)[0]]

    # Rotate coordinate system to angular momentum frame
    pos, vel = AngMomShift(pos, vel)

    # Select axes
    if axes == 'xy':
      x1 = pos[:, 0]
      x2 = pos[:, 1]
    elif axes == 'xz':
      x1 = pos[:, 0]
      x2 = pos[:, 2]
    else:
      x1 = pos[:, 1]
      x2 = pos[:, 2]

    # Plot disk and plane
    from matplotlib.colors import LogNorm
    plt.hist2d(x1, x2, bins=100, range=[[-rmax, rmax], [-rmax, rmax]], norm=LogNorm())
    ax = plt.gca()
    ax.set_axis_bgcolor('black')
    plt.gca().set_aspect('equal', adjustable='box')

    # Save figure
    frame = '%03d' % i
    figname = dirname + '/' + fgalaxy + '_' + frame + '.png'
    plt.savefig(figname)

    # Increment frame number
    i += 1


if __name__ == '__main__':

  import sys

  # Define variables
  galaxy = sys.argv[1]
  first = int(sys.argv[2])
  last = int(sys.argv[3])
  rmax = 50
  axes = 'xy'
  if len(sys.argv) == 5:
    if sys.argv[4].isdigit():
      rmax = float(sys.argv[4])
    else:
      axes = sys.argv[4]
  elif len(sys.argv) == 6:
    rmax = sys.argv[4]
    axes = sys.argv[5]

  # Execute function
  DiskRange(galaxy, first, last, rmax=rmax, axes=axes)
