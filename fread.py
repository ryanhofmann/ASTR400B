#!/usr/bin/python

# Written by Ryan Hofmann

# Import necessary modules
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


