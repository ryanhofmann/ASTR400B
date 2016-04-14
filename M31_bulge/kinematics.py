#!/usr/bin/python

# Written by Ryan Hofmann

import numpy as np
from functions import read
from functions import COM

# Define function for computing velocity statistics
def VStats(infile, axis='x', rmax=10.):

  # Read in data from file
  time, total, data = read(infile)

  # Limit selection to bulge particles
  ind = np.where(data == 3)[0]
  bulge = data[ind]

  # Compute center-of-mass position and velocity
  time, com, vcom = COM(infile, 3, tol=0.5)

  # Calibrate position and velocity relative to COM
  pos = bulge[:, 2:5] - com
  vel = bulge[:, 5:8] - vcom

  # Select only particles within rmax
  r = np.sqrt(np.sum(pos**2, axis=1))
  ind = np.where(r <= rmax)[0]
  vel = abs(vel[ind])

  # Compute mean velocity and dispersion along specified axis
  if axis == 'x':
    mean = np.mean(vel[:, 0])
    sigma = np.std(vel[:, 0])
  elif axis == 'y':
    mean = np.mean(vel[:, 1])
    sigma = np.std(vel[:, 1])
  else:
    mean = np.mean(vel[:, 2])
    sigma = np.std(vel[:, 2])
  print mean, sigma

  # Return results
  return mean, sigma
