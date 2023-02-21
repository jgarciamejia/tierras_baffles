#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 10:58:55 2020

@author: jgarciamejia

This code can de used to plot the baffle design of the Tierras Observatory. 
"""


#==============================================================================
# Load Dependencies
#==============================================================================

import baffle_func_lib as funcs
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import sys
sys.path.insert(1, '/Users/jgarciamejia/Documents/2019:20-TierrasProject/DESIGN_CODE/PWV_code')
import custom_matplotlib

#==============================================================================
# Define Mirror & Lens Shapes
# User: you need not change any values BUT ensure that 2ry mirror z-location
# matches that of the Zemax prescription version you are using!! 
#==============================================================================

### Primary Mirror - Parabolic
px,pz = 0,0                              # mm, Primary Mirror Vertex (x,z)
Rp = 5200                                # mm, Radius of Curvature of 1ry
p = Rp/2                                 # mm, Focus of Parabola @ x=0
primary_xys = np.append(np.arange(-650,-101,1),np.arange(100,651, 1))
primary_zs = - primary_xys**2 / (4*p)

### Primary Mirror Hole 
phole_xys = np.arange(-99,100,1)
phole_zs = phole_xys**2 / (4*p)

### Secondary Mirror - Hyperbolic
sx,sz = 0,-2190.99898                    # mm, Secondary Mirror Vertex (x,z)
Rs = 965.7                               # mm, Radius of Curvature of 2ry
a,b,k = 400.47125974896835, -621.880290361078, 1790.5270302510316
secondary_xys = np.arange(-114,115,1)
secondary_zs = (a/b) * np.sqrt((secondary_xys)**2 + (b)**2) - k

### Filter
# mm, diameter, radius of curv, front vertex z coordinate, thickness
d_filter, R_filter, z_filter, t_filter  = 180.4081, np.inf, 100.0, 6
# mm, Front (1) and back (2) surface x & z arrays for plotting
filter1_xys, filer1_zs = funcs.xzs_surface_generator(d_filter, z_filter, np.inf, 'plane')
filter2_xys, filer2_zs = funcs.xzs_surface_generator(d_filter, z_filter+t_filter, np.inf, 'plane')

# Lens TERR-1001
# mm, diameter, radius of curv, front vertex z coordinate, thickness
d_terr1001, R_terr1001, z_terr1001, t_terr1001  = 179.595, 180.419, 116.0002, 33.966
# mm, Front (1) and back (2) surface x & z arrays for plotting
terr1001_1_xys, terr1001_1_zs = funcs.xzs_surface_generator(d_terr1001, z_terr1001, R_terr1001, 'sphere')
terr1001_2_xys, terr1001_2_zs = funcs.xzs_surface_generator(d_terr1001, z_terr1001+t_terr1001, np.inf, 'plane')

# Lens TERR-1002
# mm, diameter front, diameter back,  radius of curv front, radius of curvature back, 
d_terr1002_1, d_terr1002_2, R_terr1002_1, R_terr1002_2 = 145.584, 128.24584, 83.87, 472.994
# mm, front vertex z coordinate, thickness
z_terr1002, t_terr1002  = z_terr1001+t_terr1001+5.96319, 47.818
# mm, Front (1) and back (2) surface x & z arrays for plotting
terr1002_1_xys, terr1002_1_zs = funcs.xzs_surface_generator(d_terr1002_1, z_terr1002, R_terr1002_1, 'sphere')
terr1002_2_xys, terr1002_2_zs = funcs.xzs_surface_generator(d_terr1002_2, z_terr1002+t_terr1002, R_terr1002_2, 'sphere')

# Lens TERR-1003
# mm, diameter front, diameter back,  radius of curv front, radius of curvature back, 
d_terr1003_1, d_terr1003_2, R_terr1003_1, R_terr1003_2 = 117.21206, 87.665237, 551.004, 53.456
# mm, front vertex z coordinate, thickness
z_terr1003, t_terr1003  = z_terr1002+t_terr1002+7.23495, 10.03400
# mm, Front (1) and back (2) surface x & z arrays for plotting
terr1003_1_xys, terr1003_1_zs = funcs.xzs_surface_generator(d_terr1003_1, z_terr1003, R_terr1003_1, 'sphere')
terr1003_2_xys, terr1003_2_zs = funcs.xzs_surface_generator(d_terr1003_2, z_terr1003+t_terr1003, R_terr1003_2, 'sphere')

# Lens TERR-1004
# mm, diameter front, diameter back,  radius of curv front, radius of curvature back, 
d_terr1004_1, d_terr1004_2, R_terr1004_1, R_terr1004_2 = 108.04594, 80.987419, 92.663, 159.993
# mm, front vertex z coordinate, thickness
z_terr1004, t_terr1004  = z_terr1003+t_terr1003+17.8479, 24.412 
# mm, Front (1) and back (2) surface x & z arrays for plotting
terr1004_1_xys, terr1004_1_zs = funcs.xzs_surface_generator(d_terr1004_1, z_terr1004, R_terr1004_1, 'sphere')
terr1004_2_xys, terr1004_2_zs = funcs.xzs_surface_generator(d_terr1004_2, z_terr1004+t_terr1004, R_terr1004_2, 'sphere')

# CCD Right Edge Location
ccd_x, ccd_z = (68.74575769/2), 288.98124 # masked semi-diagonal size
ccd_x, ccd_z = (87.0591523/2), 288.98124 # full CCD semi-diagonal size

#==============================================================================
# Iterative Steps to Find Ideal Baffle 
# Steps described in Red lab notebook, circa March 2020  
#==============================================================================
stp = 0.0001                            # mm, Resolution of rays

#==============================================================================
# ######## STEP 1: Define rays 1A and 1B, Guess Point I ########
# User: YOU must change guess_no and baffH_guess every iteration
#==============================================================================

### Rays 1A and 1B
# Ray 1A hits the primary at the max semi-field angle, u_pr, & is corresp. Ray 1B
# is reflected off of the secondary to the upper image point.

# Load Ray Data from Single Ray Trace in Zemax, Hx=1, Hy=0, Px=1, Py=0
path = '/Users/jgarciamejia/Documents/2019:20-TierrasProject/BAFFLES/'
#ray1fn = 'ray1_data.txt'
#ray1fn = 'ray1_data_c.txt' re-focused
ray1fn = 'ray1_data_p35FOV.txt' 

ray1_data = np.loadtxt(path+ray1fn, delimiter='\t', skiprows=22, max_rows=15, usecols=(0,1,2,3), encoding='utf-16')
ray1_xs = ray1_data[:,1]
ray1_zs = ray1_data[:,3]

### 2ry Baffle Height (z) Guess
guess_no = 18
baffH_guess = 315                                             # mm, desired height of baffle from 2ry vertex 
baff_h = sz+baffH_guess                                       # mm, desired coordinate of baffle bottom in z
ray1a_m, ray1a_b = funcs.define_line_from_pts(ray1_xs[0],ray1_xs[1],ray1_zs[0],ray1_zs[1])
baff_r = (baff_h - ray1a_b)/ray1a_m                           # mm, expected baffle radius and xy-coordinate
baffg_xs = np.arange(-baff_r, baff_r+stp, stp)                # mm, array defining baffle width, for plot
baffg_zs = baff_h*np.ones(len(baffg_xs))                      # mm, array defining baffle height, for plot
print ('Guess No.{}\n\nEdge of 2ry baffle is at Point 1: (x,z) = ({}, {}) mm \n'
       .format(guess_no, baff_r, baff_h))

# baff_Hguesses (with 2ry focus at z=-2190.99829): 325,330,350,355,360,400,380,375,370,365,0,320,300,310 
# baff_Hguesses (with 2ry focus at z=-2190.99777): 310, 
# baff_Hguesses (with 2ry focus at z=-2190.99898): 310, 315, 200
# baff_Hguesses (with 2ry focus at z=-2190.99898 and whole CCD FOV): 315
#==============================================================================
# ######## STEP 2, Part 1: Generate Px coordinate to trace Ray 2 in Zemax
# ######## User Note: printed values change with each iteration, but you need not modify code
#==============================================================================

# Ray 2A hits point I (edge of 2ry baffle) at the maximum downwards semi-field angle is reflected
# from the primary as ray 2B, and from the secondary to the lowest image point as ray 2C
u_pr = 0.35                                             # degrees

# Compute normalized pupil coordinate, Px (For derivation, see Mathematica NB: Baffle Calcs)
c = u_pr * (np.pi/180)         # radians, maximum semi-field angle 
m = -1/(np.tan(c))             # slope of ray 2a
x_p = -(m*Rp) - (np.sqrt(Rp)*np.sqrt(((m**2)*Rp)+(2*m*baff_r)-(2*baff_h)))     # mm, x-coord whre ray 2 hits primary
Px = x_p / 640 # normalized pupil coordinate

#print ('Open Zemax File Tierras_Can_AsBuilt_AirSpaceChange_CaF2unscratched_rays12.zmx\n')
print ('Open Zemax File Tierras_Can_AsBuilt_AirSpaceChange_CaF2unscratched_rays12c.zmx\n')
print ('Check that largest field defined = {} degrees\n'.format(u_pr))
print ('Plug in Hx=-1, Hy=0, Px = {}, Py=0 into Single Ray Trace Tool \n'.format(Px))
ray2fn = 'ray2_guess{}_data.txt'.format(guess_no)
print ('Save Ray Trace Data in Mac BAFFLES Folder as {}'.format(ray2fn))
       
# With system open in Zemax, go to Analyze > Single Ray Trace > Settings > 
# Plug in: Hx=-1, Hy=0, Px=above, Py=0 > OK > Save File as ray2_guess{}_data.txt
# For procedure details, see Baffle Notes circa April 2020

#==============================================================================
# ######## STEP 2, Part 2: Define rays 2A and 2B for plotting, then Find Point II ########
# ######## User Note: printed values change with each iteration, but you need not modify code
#==============================================================================

text = input('Data Saved? [y/n]: \n')
if text=='y': print('Proceed')
elif text=='n': print ('Code will fail')

# Load Ray 2 Data from Single Ray Trace in Zemax,
path = '/Users/jgarciamejia/Documents/2019:20-TierrasProject/BAFFLES/'
ray2_data = np.loadtxt(path+ray2fn, delimiter='\t', skiprows=22, max_rows=15, usecols=(0,1,2,3), encoding='utf-16')
ray2_xs = ray2_data[:,1]
ray2_zs = ray2_data[:,3]

# Find Point II: where 1B and 2B intersect
comm_xs = np.arange(min(ray1_xs), max(ray2_xs),stp)
Fray1 = interp1d(ray1_xs, ray1_zs, kind = 'linear')
ray1_comm_zs = Fray1(comm_xs)
Fray2 = interp1d(ray2_xs, ray2_zs, kind = 'linear')
ray2_comm_zs = Fray2(comm_xs)
idx = np.argmin(np.abs(ray1_comm_zs-ray2_comm_zs))
intrsct_1b2bx, intrsct_1b2bz = comm_xs[idx], ray1_comm_zs[idx]

# Append baff_r, baff_h to the front of ray2 array
# AFTER intersection point found! otherwise error will arise
ray2_xs = np.insert(ray2_xs, 0, baff_r)
ray2_zs = np.insert(ray2_zs, 0, baff_h)

print ('Edge of 1ry baffle is at Point 2: (x,z) = ({}, {}) mm'
       .format(intrsct_1b2bx, intrsct_1b2bz))

#==============================================================================
# ######## STEP 3, Part 1: Generate Px and Field coordinates to trace Ray 3 in Zemax
# ######## User Note: printed values change with each iteration, but you need not modify code
#==============================================================================

# Compute normalized pupil coordinate, Px2 and new field angle c2
# (For derivations, see Mathematica NB: Baffle Calcs)

m2 = funcs.define_line_from_pts(baff_r,intrsct_1b2bx,baff_h,intrsct_1b2bz)[0]
x_p2 = -(m2*Rp) - (np.sqrt(Rp)*np.sqrt(((m2**2)*Rp)+(2*m2*intrsct_1b2bx)-(2*intrsct_1b2bz)))
Px2 = x_p2 / 100         # normalized pupil coordinate
c2 = np.arctan(-1/m2)    # radians, field angle of line upon passign 1ry hole

#print ('Open Zemax File Tierras_Can_AsBuilt_AirSpaceChange_CaF2unscratched_no1ry2ry.zmx\n')
print ('Open Zemax File Tierras_Can_AsBuilt_AirSpaceChange_CaF2unscratched_no1ry2ryc.zmx\n')
print ('Define and ensure largest field has c={} degrees (X Angle)\n'.format(c2*(180/np.pi)))
print ('Plug in Hx=-1, Hy=0, Px = {}, Py=0 into Single Ray Trace Tool \n'.format(Px2))
ray3fn = 'ray3_guess{}_data.txt'.format(guess_no)
print ('Save Ray Trace Data in Mac BAFFLES Folder as {}\n'.format(ray3fn))
print ('BEWARE: There might be an IndexError due to TIR or a missed surface. Adjust max_rows below accordingly \n')

# With file _no1ry2ry open in Zemax, Add field angle = c2 from above
# then go to Analyze > Single Ray Trace > Settings > then Plug in: 
# Hx=-1, Hy=0, Px=Px2, Py=0 > OK > Save File as ray3_guess{}_data.txt
# For procedure details, see Baffle Notes circa April 2020

#==============================================================================
# ######## STEP 3, Part 2: Define ray 3A that passes through Points 1&2 for Zemax ########
# ######## User Note: values change with each iteration, but you need not modify code
#==============================================================================

text = input('Data Saved? [y/n]: \n')
if text=='y': print('Proceed')
elif text=='n': print ('Code will fail')

# Load Ray 3 Data from Single Ray Trace in Zemax,
path = '/Users/jgarciamejia/Documents/2019:20-TierrasProject/BAFFLES/'
#ray3_data = np.loadtxt(path+ray3fn, delimiter='\t', skiprows=22, max_rows=13, usecols=(0,1,2,3), encoding='utf-16')
#ray3_data = np.loadtxt(path+ray3fn, delimiter='\t', skiprows=22, max_rows=8, usecols=(0,1,2,3), encoding='utf-16') # TIR @ Surface 9
ray3_data = np.loadtxt(path+ray3fn, delimiter='\t', skiprows=22, max_rows=13, usecols=(0,1,2,3), encoding='utf-16') # TIR @ Surface 9

ray3_xs = ray3_data[:,1]
ray3_zs = ray3_data[:,3]

ray3_xs = np.insert(ray3_xs, 0, [baff_r,intrsct_1b2bx])
ray3_zs = np.insert(ray3_zs, 0, [baff_h,intrsct_1b2bz])

###### CHECKS ####
pt1x, pt1z = baff_r, baff_h
pt2x, pt2z = intrsct_1b2bx, intrsct_1b2bz

#==============================================================================
# # Format [x,y,z,l,m,n,wavenumber]
# x,y,z = baff_r, 0, baff_h
# b = np.pi/2
# c = np.arccos((pt2z-pt1z) / np.sqrt((pt2z-pt1z)**2+(pt2x-pt1x)**2))
# a = c + (np.pi/2)
# l,m,n = np.cos(a), np.cos(b), np.cos(c)
# # wavenumber is an integer indicating what wavelength to use
# # March 2020: 1 = 800 nm , 2 = 850 nm, 3 = 900 nm
# wavenumber = 2                                 
# fileline = np.array([x,y,z,l,m,n,int(wavenumber)])
# 
# # Generate RAYLIST.TXT file for Zemax
# #fname2 = 'RAYLIST_guess{0}_2rybaff{1:.0f}mm_res{2}.txt'.format(guess_no, baffH_guess,stp)
# #header2 = 'EXPLICIT'
# #np.savetxt(fname2,fileline.reshape(1,7),fmt=['%.8f','%.8f','%.8f','%.8f','%.8f','%.8f','%.0f'], 
# #           delimiter=' ', header=header2, comments='')
#==============================================================================


#==============================================================================
# Plot Results
# ######## User Note: rays 2&3 change with each iteration, but you need not modify code
#==============================================================================

fig, ax = plt.subplots(figsize=(12,12))
#plt.title('F/5.5 Baffles for Tierras Observatory, April 2020 Design, Guess No.{}'.format(guess_no), fontsize=18)

####### Mirrors #######
plt.plot([px],[pz], 'X', color='black', label='Primary Mirror Vertex, (0,0)', zorder=10)
plt.plot([sx],[sz], 'X', color='gray', label='Secondary Mirror Vertex, (0, -2190.998)')
plt.plot(primary_xys, primary_zs, color='black')
plt.plot(phole_xys, phole_zs, color='white', lw=4)
plt.plot(primary_xys, 82.52*np.ones(len(primary_xys)), color='black')
plt.plot(phole_xys, 82.52*np.ones(len(phole_xys)), color='white', lw=4)
plt.plot(secondary_xys, secondary_zs, color='gray')

####### Lenses #######
lens_color, lens_alpha = 'gray', 0.4
ax.fill_between(filter1_xys, filer1_zs, filer2_zs, facecolor='gray', alpha=0.5)
ax.fill_between(terr1001_1_xys, terr1001_1_zs, terr1001_2_zs, facecolor='gray', alpha=0.5)
ax.fill_between(terr1002_1_xys, terr1002_1_zs, np.max(terr1002_2_zs)*np.ones(len(terr1002_1_xys)), 
                facecolor=lens_color, alpha=0.5)
ax.fill_between(terr1002_2_xys, terr1002_2_zs, np.max(terr1002_2_zs)*np.ones(len(terr1002_2_xys)), 
                facecolor='white')
ax.fill_between(terr1003_1_xys, terr1003_1_zs, np.max(terr1003_2_zs)*np.ones(len(terr1003_1_xys)), 
                facecolor=lens_color, alpha=0.5)
ax.fill_between(terr1003_2_xys, terr1003_2_zs, np.max(terr1003_2_zs)*np.ones(len(terr1003_2_xys)), 
                facecolor='white')
ax.fill_between(terr1004_1_xys, terr1004_1_zs, np.max(terr1004_2_zs)*np.ones(len(terr1004_1_xys)), 
                facecolor=lens_color, alpha=0.5)
ax.fill_between(terr1004_2_xys, terr1004_2_zs, np.max(terr1004_2_zs)*np.ones(len(terr1004_2_xys)), 
                facecolor='white')
####### CCD #######
plt.plot([-ccd_x, ccd_x], [ccd_z, ccd_z], ls='-',color='gray',label='Image Plane')

####### Rays #######
plt.plot(ray1_xs, ray1_zs, ls='--', color='red', label='1AB')
plt.plot(ray2_xs, ray2_zs, ls='--', color='green', label='2ABC')
plt.plot(ray3_xs, ray3_zs, ls='--', color='blueviolet', label='3A')

# Load Ray with semi field angle above upr
# Data from Single Ray Trace in Zemax, Hx=1, Hy=0, Px=1, Py=0 
#==============================================================================
# path = '/Users/jgarciamejia/Documents/2019:20-TierrasProject/BAFFLES/'
# ray1fn = 'ray1_0.50deg2.txt'
# ray1_data = np.loadtxt(path+ray1fn, delimiter='\t', skiprows=22, max_rows=2, usecols=(0,1,2,3), encoding='utf-16')
# ray1_xs = ray1_data[:,1]
# ray1_zs = ray1_data[:,3]
# plt.plot(ray1_xs, ray1_zs, ls='--', color='goldenrod', label='1AB')
#==============================================================================

# Baffle Guesses
plt.plot(baffg_xs, baffg_zs, color='blue', label=r'2ry Baffle, h={0:.0f} mm'.format(baffH_guess))
plt.plot(baff_r, baff_h, 'o', color='blue', label='Point I')
plt.plot(intrsct_1b2bx, intrsct_1b2bz, 'o', color='blueviolet', label='Point II')

# Aesthetics
leftx, rightx = -750, 750
bottomz, topz = -2500, 500
ax.set_xlabel(r' X-Y Dimension (mm)', fontsize=20)
ax.set_ylabel(r' Z Dimension (mm) ', fontsize=20)
#ax.set_xlim(left=-120, right=120)
#ax.set_ylim(bottom=50, top=300)
ax.set_xlim(left=leftx, right=rightx)
ax.set_ylim(bottom=bottomz, top=topz)
ax.invert_yaxis()
ax.set_facecolor('white')
plt.gca().set_aspect('equal', adjustable='box')
plt.yticks(np.arange(bottomz, topz+1, 250))
ax.tick_params(direction='in', length=6, width=3, colors='black')
ax.grid(b=True, which='major', linestyle='--', lw='2', alpha=0.2)
ax.legend(fontsize = 10, loc=(1.05, 0.5),fancybox=True, framealpha=0.9)

fig.savefig('bafflespecs_guessNo.{0}_res{1}.pdf'.format(guess_no, stp))

'''
#==============================================================================
# Calculate & print inner and outer radii for primary baffle concentric disks 
# Standalone code snippet
#==============================================================================

# Load Ray Data from Single Ray Trace in Zemax, Hx=1, Hy=0, Px=1, Py=0
path = '/Users/jgarciamejia/Documents/2019:20-TierrasProject/BAFFLES/'
#ray1fn = 'ray1_data.txt'
ray1fn = 'ray1_data_c.txt'
ray1_data = np.loadtxt(path+ray1fn, delimiter='\t', skiprows=22, max_rows=15, usecols=(0,1,2,3), encoding='utf-16')
ray1_xs = ray1_data[:,1]
ray1_zs = ray1_data[:,3]

# Load Ray 2 Data from Single Ray Trace in Zemax,
guess_no = 17
path = '/Users/jgarciamejia/Documents/2019:20-TierrasProject/BAFFLES/'
ray2fn = 'ray2_guess{}_data.txt'.format(guess_no)
ray2_data = np.loadtxt(path+ray2fn, delimiter='\t', skiprows=22, max_rows=15, usecols=(0,1,2,3), encoding='utf-16')
ray2_xs = ray2_data[:,1]
ray2_zs = ray2_data[:,3]

# Define resolution and interpolate ray 1&2 data
stp = 0.0001
comm_xs = np.arange(min(ray1_xs), max(ray2_xs),stp)
Fray1 = interp1d(ray1_xs, ray1_zs, kind = 'linear')
ray1_comm_zs = Fray1(comm_xs)
Fray2 = interp1d(ray2_xs, ray2_zs, kind = 'linear')
ray2_comm_zs = Fray2(comm_xs)

# Define z location of concentric disks & find respective inner and outer radii
z_arr = np.array([-125, -250, -500, -750])
print ('  z          r_in             r_out        ')
for z in z_arr:
    rin_ind = np.argmin(np.abs((ray1_comm_zs) - z))
    rin = np.abs(comm_xs[rin_ind])
    
    rout_ind = np.argmin(np.abs((ray2_comm_zs) - z))
    rout = np.abs(comm_xs[rout_ind])
    
    print (z, rin, rout)
    
'''

'''
#==============================================================================
# Plot Ray 1 and 2ry Baffle Locations - This is a Standalone piece of code! 
#==============================================================================

# Run in BAFFLES Folder
import baffle_func_lib as funcs
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Load Ray 1 data
path = '/Users/jgarciamejia/Documents/2019:20-TierrasProject/BAFFLES/'
ray1fn = 'ray1_data.txt'
ray1_data = np.loadtxt(path+ray1fn, delimiter='\t', skiprows=22, max_rows=15, usecols=(0,1,2,3), encoding='utf-16')
ray1_xs = ray1_data[:,1]
ray1_zs = ray1_data[:,3]


# Define resolution and interpolate ray 1 data
stp = 0.00001
comm_xs = np.arange(min(ray1_xs), max(ray1_xs),stp)
Fray1 = interp1d(ray1_xs, ray1_zs, kind = 'linear')
ray1_comm_zs = Fray1(comm_xs)

# Find indices of baffles of certain radii
sx,sz = 0,-2190.99829
ind=[np.argmin(np.abs((ray1_comm_zs-sz) - 310))]
ind2=[np.argmin(np.abs((ray1_comm_zs-sz) - 375))]

# Plot
plt.plot(comm_xs, ray1_comm_zs)
plt.scatter(comm_xs[ind], ray1_comm_zs[ind])
plt.scatter(comm_xs[ind2], ray1_comm_zs[ind2])

'''