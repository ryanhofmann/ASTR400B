#!/usr/bin/python

# Written by Ryan Hofmann

import numpy as np
import matplotlib.pyplot as plt
from functions import read
from functions import COM

# Define function for plotting phase diagrams
def PhaseDiagram(infile, ptype=3, p_axis='x', v_axis='y'):

  # Read in data from file
  time, total, data = read(infile)

  # Select particles of specified type
  ind = np.where(data == ptype)[0]
  data = data[ind]

  # Normalize positions and velocities
  time, com, vcom = COM(infile, ptype, tol=0.1)
  pos = data[:, 2:5] - com
  vel = data[:, 5:8] - vcom

  # Extract relevant columns
  if p_axis == 'x':
    pos = pos[:, 0]
  elif p_axis == 'y':
    pos = pos[:, 1]
  else:
    pos = pos[:, 2]

  if v_axis == 'x':
    vel = vel[:, 0]
  elif v_axis == 'y':
    vel = vel[:, 1]
  else:
    vel = vel[:, 2]

  # Set plot limits
  p_lim, v_lim = 50., 450.

  # Plot phase diagram
  from matplotlib.colors import LogNorm
  plt.hist2d(pos, vel, range=[[-p_lim, p_lim], [-v_lim, v_lim]], bins=100, norm=LogNorm())
  p_label = p_axis+' distance (kpc)'
  v_label = v_axis+' velocity (km/s)'
  plt.xlabel(p_label)
  plt.ylabel(v_label)
  ax = plt.gca()
  ax.set_axis_bgcolor('black')
  plt.show()
