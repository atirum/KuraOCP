#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 17:04:51 2020

@author: amoolya
"""

import numpy as np
import HJB as HJB
from time import time
from numpy import pi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import h5py as h5
import os

# please add your own file anmes to plot some figures! also comment on the usetex option if you don't have latex!


plt.rcParams['text.usetex'] = True
fn = 'YOUR FN HERE'
filen = 'simDataHJBcosine.hdf5'
f1 = h5.File(fn + filen, 'r')
Y1 = f1['/']['V'][()]
xg = f1['/']['x1'][()]
yg = f1['/']['x2'][()]


sv = 2
fig = plt.figure(figsize=(10, 4))
ax1 = fig.add_subplot(121)
cont1 = ax1.contourf(xg, yg, Y1[:,:,0], levels = 10)
plt.xlabel('$\\theta_1$ (radians)', usetex=True)
plt.ylabel('$\\theta_2$ (radians)', usetex=True)
plt.title('$V_1(\\theta, 0)$', usetex=True)
plt.colorbar(cont1)

ax2 = fig.add_subplot(122)
fn = ''
filen = 'simDataHJB2.hdf5'
f1 = h5.File(fn + filen, 'r')
Y2 = f1['/']['V'][()]
xg = f1['/']['x1'][()]
yg = f1['/']['x2'][()]
cont2 = plt.contourf(xg, yg, Y2[:,:,0], levels = 10)
plt.xlabel('$\\theta_1$ (radians)', usetex=True)
plt.ylabel('$\\theta_2$ (radians)', usetex=True)
plt.title('$V_2(\\theta, 0)$', usetex=True)
plt.colorbar(cont2)

