#!/usr/bin/python

# Written by Ryan Hofmann

# Define program for calculating M(r)
def M_r(galaxy, ptype, snap, rmax):

  import numpy as np
  import math
  from COM import COM
  from fread import read

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

# If running standalone, execute function
if __name__ == '__main__':

  import sys

  # Check inputs
  if len(sys.argv) != 5 and len(sys.argv) != 6:
    print "Usage: python M_r.py galaxy ptype snap rmax [ls]"
    print "ptype = 1,2,3; 0 <= snap <= 999; rmax integer [kpc]; ls"
    exit()

  # Assign variables
  galaxy = sys.argv[1]
  ptype = int(sys.argv[2])
  snap = sys.argv[3]
  rmax = float(sys.argv[4])
  if len(sys.argv) == 6:
    ls = 1
  else:
    ls = 0

  # Execute function
  M, r = M_r(galaxy, ptype, snap, rmax)

  # Print results
  if ls:
    print r, M
  else:
    print r[-1]
    print M[-1]
