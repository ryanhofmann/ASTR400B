#!/usr/bin/python

# Written by Ryan Hofmann

# Define plotting function
def PlotBulge(infile="M31_000.txt", plane="xy", contours=0, ellipse=0):

  import numpy as np
  import matplotlib.pyplot as plt
  from functions import read
  from functions import COM

  # Read in particle data
  time, total, data = read(infile)
  index = np.where(data == 3)[0]
  bulge = data[index]

  # Compute center of mass
#  time, com, vcom = COM(infile, 3, tol=0.1)

  # Correct to center-of-mass frame
  com = np.array([-377.1, 611.05, -284.5])
  print com
  pos = bulge[:, 2:5] - com

  # Limit selection to inner 5 kpc
  r = np.sqrt(np.sum(np.square(pos), axis=1))
  index = np.where(r <= 30.)
  core = pos[index]

  # Project to specified plane
  if plane == 'xy':
    x1 = core[:, 0]
    x2 = core[:, 1]
    x = 'x'
    y = 'y'
  elif plane == 'xz':
    x1 = core[:, 0]
    x2 = core[:, 2]
    x = 'x'
    y = 'z'
  else:
    x1 = core[:, 1]
    x2 = core[:, 2]
    x = 'y'
    y = 'z'

  # Plot disk particles
  from matplotlib.colors import LogNorm
  plt.hist2d(x1, x2, bins=300, norm=LogNorm())
  plt.xlabel(x+' (kpc)')
  plt.ylabel(y+' (kpc)')
  plt.colorbar()

  # Overplot contours
  if contours:
    angle = np.linspace(0, 2*np.pi, 100)
    for r in [0.5, 1.0, 1.5, 2.0, 3.0, 4.0]:
      a, b = r, r
      plt.plot(a*np.cos(angle), b*np.sin(angle), linewidth=2.0, color='k')

  # Show plot
  r = 5.0
  plt.axis([-r, r, -r, r])
  plt.gca().set_aspect('equal', adjustable='box')
  plt.show()
