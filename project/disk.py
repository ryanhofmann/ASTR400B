#!/usr/bin/python

# Written by Ryan Hofmann

from functions import read
from functions import COM
import numpy as np
import matplotlib.pyplot as plt

# Define function for fitting plane to disk
def DiskPlane(infile, axes='xy'):

  # Compute COM
  time, com, vcom = COM(infile, 2, tol=0.5)

  # Read in disk data
  time, total, data = read(infile)
  disk = data[np.where(data == 2)[0]]

  # Shift to COM frame
  pos = data[:, 2:5] - com
  vel = data[:, 5:8] - vcom

  # Select relevant region
  lim = 40
  r = np.sqrt(np.sum(np.square(pos), axis=1))
  pos = pos[np.where(r < lim)]
  vel = vel[np.where(r < lim)]

  # Compute direction of angular momentum vector
  L = np.sum(np.cross(pos, vel), axis=0)
  L_norm = L/np.sqrt(np.sum(L**2))

  # Set up rotation matrix to map norm to z unit vector (disk in xy-plane)
  z_norm = np.array([0, 0, 1])
  v = np.cross(L_norm, z_norm)
  s = np.sqrt(np.sum(v**2))
  c = np.dot(L_norm, z_norm)
  I = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
  v_x = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
  R = I + v_x + np.dot(v_x, v_x)*(1 - c)/s**2

  # Rotate coordinate system
  rot = []
  for point in pos:
    rot.append(np.dot(R, point))
  pos = np.array(rot)

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
  plt.hist2d(x1, x2, bins=100, norm=LogNorm())
  ax = plt.gca()
  ax.set_axis_bgcolor('black')
  plt.gca().set_aspect('equal', adjustable='box')
  plt.colorbar()
  plt.show()


if __name__ == '__main__':

  import sys

  if len(sys.argv) == 2:
    DiskPlane(sys.argv[1])
  elif len(sys.argv) == 3:
    DiskPlane(sys.argv[1], axes=sys.argv[2])
