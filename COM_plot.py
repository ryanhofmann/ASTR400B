#!/usr/bin/python

# Written by Ryan Hofmann

# Define plotting function
def sep_plot(galaxy1, galaxy2, v=False):

  # Import necessary modules
  import numpy as np
  import matplotlib.pyplot as plt
  from COMread import COMread

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

# Execute function
if __name__ == '__main__':

  # Import necessary modules
  import numpy as np
  import sys

  # Check inputs
  if len(sys.argv) != 3 and len(sys.argv) != 4:
    print "Usage: python COM_plot.py galaxy1 galaxy2 [v]"
    exit()

  # Assign variables
  galaxy1 = sys.argv[1]
  galaxy2 = sys.argv[2]
  v = False
  if len(sys.argv) == 4 and 'v' in sys.argv[3]:
    v = True

  # Run function
  sep_plot(galaxy1, galaxy2, v)
