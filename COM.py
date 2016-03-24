#!/usr/bin/python

# Written by Ryan Hofmann

# Define function for computing COM
def COM(fname, ptype, tol=2):

  from fread import read
  import numpy as np

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
