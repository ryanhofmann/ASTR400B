#!/usr/bin/python

# Written by Ryan Hofmann

from functions import read
from functions import COM
import numpy as np
import matplotlib.pyplot as plt

# Define function for rotating disk to angular momentum frame
# Takes as inputs position and velocity arrays in COM frame
def AngMomShift(pos, vel):

  # Select central region of disk
  L_lim = 5
  r = np.sqrt(np.sum(np.square(pos), axis=1))
  L_pos = pos[np.where(r < L_lim)[0]]
  L_vel = vel[np.where(r < L_lim)[0]]

  # Compute direction of angular momentum vector
  L = np.sum(np.cross(L_pos, L_vel), axis=0)
  L_norm = L/np.sqrt(np.sum(L**2))

  # Set up rotation matrix to map L_norm to z unit vector (disk in xy-plane)
  z_norm = np.array([0, 0, 1])
  v = np.cross(L_norm, z_norm)
  s = np.sqrt(np.sum(v**2))
  c = np.dot(L_norm, z_norm)
  I = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
  v_x = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
  R = I + v_x + np.dot(v_x, v_x)*(1 - c)/s**2

  # Rotate coordinate system
  pos = np.dot(R, pos.T).T
  vel = np.dot(R, vel.T).T

  # Return rotated postion and velocity arrays
  return pos, vel


# Define function for plotting disk
def DiskPlot(pos, axes='xy'):

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
  r = np.max(x1)
  from matplotlib.colors import LogNorm
  plt.hist2d(x1, x2, bins=100, range=[[-r, r], [-r, r]], norm=LogNorm())
  ax = plt.gca()
  ax.set_axis_bgcolor('black')
  plt.gca().set_aspect('equal', adjustable='box')
  plt.colorbar()
  plt.show()


if __name__ == '__main__':

  import sys

  # Define arguments
  infile = sys.argv[1]
  if len(sys.argv) == 3:
    axes = sys.argv[2]
  else:
    axes = 'xy'

  # Read in data from file
  time, total, data = read(infile)

  # Compute COM and shift to COM frame
  time, com, vcom = COM(infile, 3, tol=0.5)
  pos = data[:, 2:5] - com
  vel = data[:, 5:8] - vcom

  # Select only disk particles
  ind = np.where(data == 2)[0]
  pos = pos[ind]
  vel = vel[ind]

  # Select region for plotting
  rmax = 50
  r = np.sqrt(np.sum(np.square(pos), axis=1))
  pos = pos[np.where(r < rmax)[0]]
  vel = vel[np.where(r < rmax)[0]]

  # Rotate coordinate system to angular momentum frame
  pos, vel = AngMomShift(pos, vel)

  # Plot disk in specified plane
  DiskPlot(pos, axes)
