#!/usr/bin/python

# Written by Ryan Hofmann

from functions import read
from functions import COM
import numpy as np
import matplotlib.pyplot as plt
from disk import AngMomShift

# Define function for plotting disk with z and vz histograms
def DiskStatPlot(galaxy, snap, dirname='.', fnum=0, rmax=50):

  # Construct filename
  infile = galaxy + '_%03d.txt' % snap

  # Read in data from file
  time, total, data = read(infile)

  # Compute COM and shift to COM frame
  time, com, vcom = COM(infile, 3, tol=0.5)
  pos = data[:, 2:5] - com
  vel = data[:, 5:8] - vcom

  # Select only disk particles
  ind = np.where(data == 2)[0]
  pos, vel = pos[ind], vel[ind]

  # Select region for plotting
  r = np.sqrt(np.sum(np.square(pos), axis=1))
  ind = np.where(r < rmax)[0]
  pos, vel = pos[ind], vel[ind]

  # Rotate coordinate system to angular momentum frame
  pos, vel = AngMomShift(pos, vel)

  # Plot disk with statistics
  from matplotlib.colors import LogNorm
  plt.subplot(221) # xy-plane
  plt.hist2d(pos[:, 0], pos[:, 1], range=[[-rmax, rmax], [-rmax, rmax]], bins=100, norm=LogNorm())
  ax = plt.gca()
  ax.set_axis_bgcolor('black')
  ax.set_aspect('equal', adjustable='box')
  plt.xlabel('x (kpc)')
  plt.ylabel('y (kpc)')
  title = 't = ' + '%d' % time + ' Myr'
  ax.set_title(title)

  plt.subplot(223) # xz-plane
  plt.hist2d(pos[:, 0], pos[:, 2], range=[[-rmax, rmax], [-rmax, rmax]], bins=100, norm=LogNorm())
  ax = plt.gca()
  ax.set_ylim([-rmax, rmax])
  ax.set_axis_bgcolor('black')
  ax.set_aspect('equal', adjustable='box')
  plt.xlabel('x (kpc)')
  plt.ylabel('z (kpc)')

  plt.subplot(222) # z histogram
  z_disp = np.std(pos[:, 2])
  zrange = 3*z_disp
  plt.hist(pos[:, 2], bins=100, range=[-zrange, zrange])
  plt.xlabel('z (kpc)')
  ax = plt.gca()
  ax.set_xlim([-zrange, zrange])

  plt.subplot(224) # vz histogram
  vz_disp = np.std(vel[:, 2])
  vzrange = 3*vz_disp
  plt.hist(vel[:, 2], bins=100, range=[-vzrange, vzrange])
  plt.xlabel(r'v$_z$ (km s$^{-1}$)')
  ax = plt.gca()
  ax.set_xlim([-vzrange, vzrange])

  # Save plot
  frame = '%03d' % fnum
  if '/' in galaxy:
    fgalaxy = galaxy.split('/')[-1]
  else:
    fgalaxy = galaxy
  figname = dirname + '/' + fgalaxy + '_' + frame + '.png'
  plt.savefig(figname)
  plt.clf()

  # Return time and dispersion values
  return time, z_disp, vz_disp


# Define function for plotting disk and stats over time range
def DiskStatRange(galaxy, first, last, rmax=50):

  # Create directory for saving data
  firststr, laststr = '%03d' % first, '%03d' % last
  if '/' in galaxy:
    fgalaxy = galaxy.split('/')[-1]
  else:
    fgalaxy = galaxy
  dirname = fgalaxy + '_' + firststr + '_' + laststr + '_stats'
  print dirname
  import os
  if not os.path.isdir(dirname):
    os.makedirs(dirname)

  # Loop over snap range
  i = 0
  time = np.zeros(last - first + 1)
  z_disp = np.zeros(last - first + 1)
  vz_disp = np.zeros(last - first + 1)
  for snap in range(first, last+1):
    print fgalaxy, snap, i
    time[i], z_disp[i], vz_disp[i] = DiskStatPlot(galaxy, snap, dirname, i, rmax=rmax)
    i += 1

  # Write dispersions to text file
  DATA = np.column_stack((time, z_disp, vz_disp))
  header = "Time\tz_disp\tvz_disp"
  outfile = dirname + '/' + fgalaxy + '_dispersions.txt'
  np.savetxt(outfile, DATA, header=header, fmt='%.3f', delimiter='\t')

  # Plot dispersions
  plt.plot(z_disp, vz_disp, marker='+')
  plt.xlabel('z dispersion (kpc)')
  plt.ylabel('v dispersion (km/s)')

  # Save dispersion plot
  figname = dirname + '/' + fgalaxy + '_dispersions.png'
  plt.savefig(figname)


if __name__ == '__main__':

  import sys

  # Define variables
  galaxy = sys.argv[1]
  first = int(sys.argv[2])
  last = int(sys.argv[3])
  rmax = 50
  if len(sys.argv) == 5:
    rmax = int(sys.argv[4])

  # Execute function
  DiskStatRange(galaxy, first, last, rmax=rmax)
