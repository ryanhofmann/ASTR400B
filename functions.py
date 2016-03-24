#!/usr/bin/python

# Written by Ryan Hofmann

import numpy as np

# Define function for reading data from file
def read( fname ):

  # Open file for reading
  infile = open(fname, "r")

  # Get time
  line = infile.readline()
  words = line.split()
  time = float(words[1])

  # Get number of particles
  line = infile.readline()
  words = line.split()
  total = float(words[1])

  # Close file
  infile.close()

  # Read data into array
  array = np.genfromtxt(fname, skip_header=4, autostrip=True)

  # Return time, total, and array as output
  return time, total, array;


# Define function for computing COM
def COM(fname, ptype, tol=2):

  # Read in data
  time, total, data = read(fname)

  # Extract relevant data
  data = np.array([item[1:8] for item in data if item[0] == ptype])

  # Define variables for COM calculation
  m = data[:,0]
  x = data[:,1]
  y = data[:,2]
  z = data[:,3]
  vx = data[:,4]
  vy = data[:,5]
  vz = data[:,6]
  xcom, ycom, zcom, vxcom, vycom, vzcom = 0, 0, 0, 0, 0, 0

  # Compute COM iteratively until tol is met
  for n in range(0, 100):

    # Compute COM coordinates
    x0, y0, z0 = xcom, ycom, zcom
    xcom = sum(x*m)/sum(m)
    ycom = sum(y*m)/sum(m)
    zcom = sum(z*m)/sum(m)

    # Compute COM velocity
    vx0, vy0, vz0 = vxcom, vycom, vzcom
    vxcom = sum(vx*m)/sum(m)
    vycom = sum(vy*m)/sum(m)
    vzcom = sum(vz*m)/sum(m)
#    print vxcom, vycom, vzcom

    # Find maximum distance from COM
    dx = x - xcom
    dy = y - ycom
    dz = z - zcom
    r = np.sqrt(dx**2 + dy**2 + dz**2)
    rmax = np.max(r)
#    print rmax

    # Check tol, exit if met
    xshift = xcom - x0
    yshift = ycom - y0
    zshift = zcom - z0
    dif = np.sqrt(xshift**2 + yshift**2 + zshift**2)
    if dif < tol:
      break

    # If tol not met, reduce sample radius
    ind = np.where(r < rmax/2)[0]
    m = m[ind]
    x = x[ind]
    y = y[ind]
    z = z[ind]
    vx = vx[ind]
    vy = vy[ind]
    vz = vz[ind]
#    print len(ind)
    if len(ind) < 100:
      print "Error: tol not met"
      break

  # Return result
  com = [xcom, ycom, zcom]
  vcom = [vxcom, vycom, vzcom]
  return time, com, vcom


# Define function for reading COM data file
def COMread(galaxy):

  import numpy as np

  # Construct file name
  fname = 'COM_'+galaxy+'.txt'

  # Read in data
  data = np.genfromtxt(fname, dtype=None)

  # Return arrays
  time = data[:,0]
  com = data[:,1:4]
  vcom = data[:,4:7]
  return time, com, vcom


# Define separation plotting function
def sep_plot(galaxy1, galaxy2, v=False):

  import matplotlib.pyplot as plt

  # Read in COM data
  time, com1, vcom1 = COMread(galaxy1)
  time, com2, vcom2 = COMread(galaxy2)

  # Compute separation magnitudes
  if v:
    diff = vcom2 - vcom1
  else:
    diff = com2 - com1
  sep = np.sqrt(np.sum(diff**2, axis=1))

  # Plot separation vs time
  plt.plot(time, sep, 'bo')
  plt.xlabel('time (Myr)')
  if v:
    plt.ylabel('relative velocity (km/s)')
  else:
    plt.ylabel('separation (kpc)')
  plt.show()


# Define particle plotting function
def disk_plot(galaxy, snap, plane='xy'):

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


# Define program for calculating M(r)
def M_r(galaxy, ptype, snap, rmax):

  import math

  # Construct file name
  str1 = snap.zfill(3)
  fin = galaxy+'_'+str1+'.txt'

  # Read file and calculate COM
  time, com, vcom = COM(fin, ptype)
  time, total, data = read(fin)
  data = [item for item in data if item[0] == ptype]

  # Compute enclosed mass
  n = 1 + int(rmax)
  r = np.array(range(0, n))
  M = np.array([0.0]*n)
  pos = np.array(data)[:,[2,3,4]]
  x = pos - com
  distance = np.sqrt(np.sum(x*x, 1))
  print np.max(distance)
  data = np.insert(data, 5, distance, axis=1)
  for i in range(0, n):
    M[i] += sum([item[1] for item in data if item[5] < r[i]])

  # Return enclosed mass and radius
  return r, M


# Define function for computing circular velocity
def v_r(galaxy, ptype, snap, rmax):

  # Calculate M(r)
  r, M = M_r(galaxy, ptype, snap, rmax)

  # Compute v(r) = sqrt(G*M(r)/r)
  G = 4.30e-6 # [kpc/Msun]*[km/s]^2
  v = np.sqrt(G*M*1e10/(r + 1e-10))

  # Return v(r) and M(r)
  return r, M, v

