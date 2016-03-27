#!/usr/bin/python

# Written by Ryan Hofmann

# Define function for computing circular velocity
def v_r(galaxy, ptype, snap, rmax):

  import numpy as np
  from M_r import M_r

  # Calculate M(r)
  r, M = M_r(galaxy, ptype, snap, rmax)

  # Compute v(r) = sqrt(G*M(r)/r)
  G = 4.30e-6 # [kpc/Msun]*[km/s]^2
  v = np.sqrt(G*M*1e10/(r + 1e-10))

  # Return v(r) and M(r)
  return r, M, v

# If running standalone, execute function
if __name__ == '__main__':

  import sys

  # Check inputs
  if len(sys.argv) != 5:
    print "Usage: python v_r.py galaxy ptype snap rmax"
    print "ptype = 1,2,3; 0 <= snap <= 999"
    exit()

  # Define variables
  galaxy = sys.argv[1]
  ptype = int(sys.argv[2])
  snap = sys.argv[3]
  rmax = float(sys.argv[4])

  # Execute function
  r, M, v = v_r(galaxy, ptype, snap, rmax)

  # Print results
  print r
  print v
