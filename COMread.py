#!/usr/bin/python

# Written by Ryan Hofmann

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
