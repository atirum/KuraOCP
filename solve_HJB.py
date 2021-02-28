"""
Created on Thu Dec 17 19:21:47 2020

@author: amoolya
"""


import numpy as np
import HJB as HJB
from numpy import pi
import matplotlib.pyplot as plt
# import h5py as h5
# import os
######################################################
#
#
# this sets up the computation grid. we exclude the 
# last point because we are on the torus, so the 
# first point is the same as the M+1th point
#
######################################################
M = 40
x1 = np.linspace(0,2*pi,num=M, endpoint=False)
x2 = np.linspace(0,2*pi,num=M, endpoint=False)
x1g, x2g = np.meshgrid(x1, x2)
phi = np.zeros((2,M,M))
phi[0, :, :] = 1 + np.sin(x2g - x1g)
phi[1, :, :] = 1 + np.sin(x1g - x2g)
dx = np.mean(np.diff(x1))
#####################################################
#
# match your timestep value with the SDE simulation
# or you'll have to interpolate in time, as well!
#
#
#####################################################
dt = 5e-4
T = 5/dt
VT = np.zeros((M,M))
######################################################
#
#
# you can set your own Lagrangian function on the 
# state variable here!
#
######################################################
# Lag = 3*x1g + 3*x2g
Lag = 20*(1 + np.cos(x1g - x2g))
# VT = np.zeros((M,M))
lam = .5
######################################################
#
#
# we set up the points to interpolate over here. 
# these are passed into fortran and used in the 
# interpolation there.
#
######################################################
theta = np.zeros((2,M))
theta[0,:] = x1
theta[1,:] = x2
thetap = np.zeros((4,2,M))
thetap[0,0,:] = np.mod(x1 + 1, 2*pi)
thetap[0,1,:] = x2
thetap[1,0,:] = np.mod(x1 - 1, 2*pi)
thetap[1,1,:] = x2
thetap[2,0,:] = x1
thetap[2,1,:] = np.mod(x2 + 1, 2*pi)
thetap[3,0,:] = x1
thetap[3,1,:] = np.mod(x2 - 1, 2*pi)
V = HJB.solve_hjb(T, dx, dt, VT, theta, thetap, phi, Lag, lam)
gradV = np.gradient(V,dx,axis=(0,1))
plt.contourf(x1g, x2g, V[:,:,0], 30)
###################################################################
#
#
# please put your file location here if you want to save!
#
###################################################################
# fn = 'FN GOES HERE'
# filen = 'simDataHJBcosine.hdf5'
# if os.path.isfile(fn + filen):
#     os.remove(fn + filen)
# datafile = h5.File(fn + filen, 'w')
# datafile.create_dataset('V', data=V)
# datafile.create_dataset('gradV', data=gradV)
# datafile.create_dataset('x1', data=x1g)
# datafile.create_dataset('x2', data=x2g)
# datafile.create_dataset('theta1', data=x1)
# datafile.create_dataset('theta2', data=x2)
# datafile.close
