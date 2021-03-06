#!/usr/bin/python

# Written by Ryan Hofmann

import numpy as np

# Gravitational constant
G = 4.498768e-6 # kpc^3 Msun^-1 Gyr^-2

# Define Hernquist acceleration function (halo and bulge)
def HernquistAccel(M, r_a, x, j): # Msun, kpc, j=1,2,3

  # Compute total distance r
  r = np.sqrt(x[0]**2 + x[1]**2 + x[2]**2)

  # Compute jth component of acceleration (kpc Gyr^-2)
  a_j = -G*M/(r*(r_a + r)**2)*x[j-1]

  # Return result
  return a_j


# Define Miyamoto-Nagai acceleration function (disk)
def MiyamotoNagaiAccel(M, r_d, x, j): # Msun, kpc, j=1,2,3

  # Compute components R and B
  R = np.sqrt(x[0]**2 + x[1]**2)
  z_d = r_d/5.
  B = r_d + np.sqrt(x[2]**2 + z_d**2)

  # Compute jth component of acceleration (kpc Gyr^-2)
  if j == 1 or j == 2:
    a_j = -G*M*x[j-1]/(R**2 + B**2)**1.5
  if j == 3:
    a_j = -G*M*B*x[2]/((R**2 + B**2)**1.5 * np.sqrt(x[2]**2 + z_d**2))

  # Return result
  return a_j


# Define dynamical friction function
def DynamicalFriction(Msat, x, v, j):

  # Define Coulomb logarithm
  r = np.sqrt(x[0]**2 + x[1]**2 + x[2]**2)
  bmax = r
  bmin = G*Msat/(M31Vcirc(x))**2
  Lambda = bmax/bmin

  # Compute acceleration
  V = np.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
  a_j = -0.428*(G*Msat*np.log(Lambda)/r**2)*v[j-1]/V

  # Return result
  return a_j


# Define full acceleration function
def M31Accel(x, v): # kpc, kpc/Gyr

  # Define all component masses (M_sun)
  M_disk = 0.12e12
  M_bulge = 0.019e12
  M_halo = 1.921e12
  Msat = 0.196e12

  # Define all component scale sizes (kpc)
  r_disk = 5.
  r_bulge = 1.
  r_halo = 62.

  # Initialize acceleration vector
  a = np.zeros(3)

  # Compute acceleration (kpc Gyr^-2)
  for j in [1,2,3]:
    a[j-1] += HernquistAccel(M_halo, r_halo, x, j)
    a[j-1] += HernquistAccel(M_bulge, r_bulge, x, j)
    a[j-1] += MiyamotoNagaiAccel(M_disk, r_disk, x, j)
    a[j-1] += DynamicalFriction(Msat, x, v, j)

  # Return acceleration vector
  return a


# Define Hernquist circular speed function
def HernquistVcirc(M, r_a, x): # M_sun, kpc

  # Compute total distance r (kpc)
  r = np.sqrt(x[0]**2 + x[1]**2 + x[2]**2)

  # Compute circular velocity (kpc/Gyr)
  v_circ = np.sqrt(G*M*r/(r + r_a)**2)

  # Return result
  return v_circ


# Define Miyamoto-Nagai circular speed function
def MiyamotoNagaiVcirc(M, r_d, x): # M_sun, kpc

  # Compute xy-distance, total distance, and z_d (kpc)
  R = np.sqrt(x[0]**2 + x[1]**2)
  r = np.sqrt(R**2 + x[2]**2)
  z_d = r_d/5.

  # Compute circular velocity (kpc/Gyr)
  v_circ = np.sqrt(G*M*r**2/(R**2 + (r_d + z_d)**2)**1.5)

  # Return result
  return v_circ


# Define total circular velocity function
def M31Vcirc(x): # kpc

  # Define all component masses (M_sun)
  M_disk = 0.12e12
  M_bulge = 0.019e12
  M_halo = 1.921e12

  # Define all component scale sizes (kpc)
  r_disk = 5.
  r_bulge = 1.
  r_halo = 62.

  # Compute circular velocity
  v_halo = HernquistVcirc(M_halo, r_halo, x)
  v_bulge = HernquistVcirc(M_bulge, r_bulge, x)
  v_disk = MiyamotoNagaiVcirc(M_disk, r_disk, x)
  v_circ = np.sqrt(v_halo**2 + v_bulge**2 + v_disk**2)

  # Return result
  return v_circ


# Define leapfrog integrator function
def LeapFrog(dt, x, v): # Gyr, kpc, kpc/Gyr

  # Compute position at 1/2 timestep (kpc)
  x_mid = x + v*dt/2

  # Compute acceleration at 1/2 timestep (kpc Gyr^-2)
  a_mid = M31Accel(x_mid, v)

  # Compute velocity at full timestep (kpc/Gyr)
  v_new = v + a_mid*dt

  # Compute position at full timestep (kpc)
  x_new = x + 0.5*(v + v_new)*dt

  # Return updated position and velocity
  return x_new, v_new


# Define write function for orbit output
def write(f, t, x, v):

  # Convert numbers to strings, 4 significant digits
  t_s = '%s' % float('%.4g' % t)
  x_s = '%s' % float('%.4g' % x[0])
  y_s = '%s' % float('%.4g' % x[1])
  z_s = '%s' % float('%.4g' % x[2])
  vx_s = '%s' % float('%.4g' % v[0])
  vy_s = '%s' % float('%.4g' % v[1])
  vz_s = '%s' % float('%.4g' % v[2])
  string = t_s+'\t'+x_s+'\t'+y_s+'\t'+z_s+'\t'+vx_s+'\t'+vy_s+'\t'+vz_s+'\n'
  f.write(string)


# Define orbit integration function
def OrbitIntegrator(t_0, dt, t_max, real=1): # Gyr

  if real:
    # Define initial real values
    x_M31 = np.array([-378., 611., -285.])
    x_M33 = np.array([-476., 491., -412.])
    x = x_M33 - x_M31
    v_M31 = np.array([74., -72., 49.])
    v_M33 = np.array([43., 102., 142.])
    v = v_M33 - v_M31
  else:
    # Define initial circular values
    x = np.array([30., 0., 0.])
    v = np.array([0., M31Vcirc(x), 0.])

  # Convert initial velocity to kpc/Gyr
  v = (3.1536/3.0857)*v

  # Open file for writing
  if real:
    f = open("orbits_real.txt", "w")
  else:
    f = open("orbits_circ.txt", "w")

  # Write header to file
  string = "Time\tx\ty\tz\tvx\tvy\tvz\n"
  f.write(string)

  # Write initial values to file
  write(f, t_0, x, v)

  # Integrate orbit
  t = t_0
  while t < t_max:
    t += dt
    x, v = LeapFrog(dt, x, v)
    write(f, t, x, v)

  # Return final values
  return t, x, v



# Define plotting function
def plot(infile='orbits.txt', vel=0):

  # Read data from file
  array = np.genfromtxt(infile, skip_header=1)

  # Define arrays for plotting
  t = array[:,0]
  if vel:
    # Compute total speed
    vx = array[:,4]
    vy = array[:,5]
    vz = array[:,6]
    v = np.sqrt(vx**2 + vy**2 + vz**2)
  else:
    # Compute total distance
    x = array[:,1]
    y = array[:,2]
    z = array[:,3]
    r = np.sqrt(x**2 + y**2 + z**2)

  # Plot data
  import matplotlib.pyplot as plt
  if vel:
    plt.plot(t, v)
    plt.ylabel(r'Speed ($kpc\ Gyr^{-1}$)')
    plt.title('Speed vs. Time')
  else:
    plt.plot(t, r)
    plt.ylabel(r'Distance ($kpc$)')
    plt.title('Distance vs. Time')
  plt.xlabel(r'Time ($Gyr$)')
  plt.show()

