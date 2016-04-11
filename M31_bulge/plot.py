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

  # Project to specified plane
  if plane == 'xy':
    x1 = pos[:, 0]
    x2 = pos[:, 1]
    x = 'x'
    y = 'y'
  elif plane == 'xz':
    x1 = pos[:, 0]
    x2 = pos[:, 2]
    x = 'x'
    y = 'z'
  else:
    x1 = pos[:, 1]
    x2 = pos[:, 2]
    x = 'y'
    y = 'z'

  # Plot disk particles
  from matplotlib.colors import LogNorm
  r = 5.
  plt.hist2d(x1, x2, range=[[-r, r], [-r, r]], bins=100, norm=LogNorm())
  plt.xlabel(x+' (kpc)')
  plt.ylabel(y+' (kpc)')
  plt.colorbar()

  # Overplot contours
  if contours:
    angle = np.linspace(0, 2*np.pi, 100)
    r = np.array([0.5, 1.0, 1.5, 2.0, 3.0, 4.0])
    if plane == 'xy' and ellipse:
      e = np.array([0.06, 0.24, 0.28, 0.28, 0.23, 0.18])
      q = -1*e + 1.
      print q
      k = -0.3
    elif plane == 'xz' and ellipse:
      e = np.array([0.06, 0.22, 0.28, 0.28, 0.19, 0.18])
      q = -1*e + 1.
      print q
      k = -0.32
    elif ellipse:
      e = np.zeros(6)
      k = 0.
    for i in range(0, len(r)):
      if ellipse:
        a = r[i]/np.sqrt(1. - e[i])
        b = r[i]*np.sqrt(1. - e[i])
      else:
        a, b = r[i], r[i]
      x1, x2 = a*np.cos(angle), b*np.sin(angle)
      if ellipse:
        x1_r = x1*np.cos(k) - x2*np.sin(k)
        x2_r = x2*np.cos(k) + x1*np.sin(k)
        x1, x2 = x1_r, x2_r
      plt.plot(x1, x2, linewidth=2.0, color='k')

  # Show plot
  r = 5.0
  plt.axis([-r, r, -r, r])
  ax = plt.gca()
  ax.set_axis_bgcolor('black')
  plt.gca().set_aspect('equal', adjustable='box')
  plt.show()
