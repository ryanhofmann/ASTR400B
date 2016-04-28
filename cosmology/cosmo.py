#!/usr/bin/python

# Written by Ryan Hofmann

import numpy as np

# Declare global variables
h = 0.6781
H0 = 100*h
h_fac = 1.02268944e-3
c = 2.99792458e5

# Define function for computing Hubble parameter
def H(z, m0=0.308, lambda0=0.692, rad0=8.24e-5, h=0.6781):

  H0 = 100*h
  return H0*np.sqrt(m0*(1 + z)**3 + lambda0 + rad0*(1 + z)**4)


# Define function for computing lookback time
def LBT(zmax, m0=0.308, lambda0=0.692, rad0=8.24e-5, h=0.6781):

  from scipy.integrate import simps

  zrange = np.arange(0, zmax, 1e-3)
  def y(z):
    return 1./H(z, m0=m0, lambda0=lambda0, rad0=rad0, h=h*h_fac)/(1+z)

  t = simps(y(zrange), zrange)

  return t


def LBTplot(zmax, step, benchmark=1):

  if benchmark==0:
    m0, lambda0, rad0 = 1, 0, 0
  else:
    m0=0.308; lambda0=0.692; rad0=8.24e-5

  z = np.arange(step, zmax+step, step)
  t = np.zeros(zmax/step)
  for i in range(0, len(z)):
    t[i] = LBT(z[i], m0=m0, lambda0=lambda0, rad0=rad0)
  import matplotlib.pyplot as plt
  plt.plot(z, t)
  plt.show()


def CD(zmax, m0=0.308, lambda0=0.692, rad0=8.24e-5, h=0.6781):

  from scipy.integrate import simps

  zrange = np.arange(0, zmax, 1e-3)
  def y(z):
    return c/H(z, m0=m0, lambda0=lambda0, rad0=rad0, h=h)

  D_C = simps(y(zrange), zrange)

  return D_C


def Distances(z, m0=0.308, lambda0=0.692, rad0=8.24e-5, h=0.6781):

  D_C = CD(z)
  D_L = D_C*(1 + z)
  D_A = D_C/(1 + z)

  print "Comoving distance:", D_C
  print "Luminosity distance:", D_L
  print "Angular diameter distance:", D_A

  return D_C, D_L, D_A


