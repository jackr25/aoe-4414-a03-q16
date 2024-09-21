# sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
#  Converts coordinate transform from SEZ frame to ECEF. 
# Parameters:
# o_lat_deg 
# o_lon_deg 
# o_hae_km 
# s_km 
# e_km 
# z_km
# Output:
#  Prints the vector now in ECEF coord sys.
#
# test case input: python3 sez_to_ecef.py 40.496 -80.246 0.37 0 1 0.3
#
# Written by Jack Rathert
# Other contributors: None


# import Python modules
import sys 
import numpy as np
from numpy import cos,sin 

# "constants"
# e.g., R_E_KM = 6378.137

# helper functions

## function description
def calc_rotations(th_deg, ph_deg, rs, re, rz):
  th = th_deg*np.pi/180
  ph = ph_deg*np.pi/180
  return np.array([cos(th)*sin(ph)*rs + cos(th)*cos(ph)*rz-sin(th)*re, sin(th)*sin(ph)*rs + sin(th)*cos(ph)*rz + cos(th)*re, -cos(ph)*rs + sin(ph)*rz])


def calc_llh_to_ecef(lat_deg, lon_deg, hae_km):
  R_E_KM = 6378.1363
  E_E = 0.081819221456
  
  lat_rad = lat_deg*np.pi/180.0
  lon_rad = lon_deg*np.pi/180.0

  denom = np.sqrt(1-E_E**2 *(sin(lat_rad))**2)

  C_E = R_E_KM/denom
  S_E = R_E_KM*(1-E_E**2)/denom

  r_x_km = (C_E + hae_km)*cos(lat_rad)*cos(lon_rad)
  r_y_km = (C_E + hae_km)*cos(lat_rad)*sin(lon_rad)
  r_z_km = (S_E + hae_km)*sin(lat_rad)

  return np.array([r_x_km, r_y_km, r_z_km])

# initialize script arguments
o_lat_deg = float('nan')
o_lon_deg = float('nan')
o_hae_km = float('nan')
s_km = float('nan')
e_km = float('nan')
z_km = float('nan')

# parse script arguments
if len(sys.argv)==7:
  o_lat_deg = float(sys.argv[1])
  o_lon_deg = float(sys.argv[2])
  o_hae_km = float(sys.argv[3])
  s_km = float(sys.argv[4])
  e_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
   'Usage: '\
   'python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km'\
  )
  exit()

# write script below this line

r_ecef_obs = calc_llh_to_ecef(o_lat_deg, o_lon_deg, o_hae_km)
r_ecef = calc_rotations(o_lon_deg, o_lat_deg, s_km, e_km, z_km)

r_ecef_total = r_ecef_obs + r_ecef

print(r_ecef_total[0])
print(r_ecef_total[1])
print(r_ecef_total[2])