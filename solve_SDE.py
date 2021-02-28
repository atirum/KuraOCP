"""
Created on Wed Dec 23 00:11:21 2020

@author: amoolya
"""

import numpy as np
# import scipy as sp
import scipy.stats as sps
import matplotlib.pyplot as plt
from numpy import pi
# import h5py as h5

# simulation of an M-dimensional Poisson process
def sim_poisson(M, dt, tf, rate):
    T = np.int32(tf/dt)
    rn = np.random.rand(M, T)
    p = 1 - np.exp(-rate*dt)
    dN = np.int32(rn < p)
    return(dN)

def f(theta, omega1, omega2, K1, K2):
    f = np.zeros(2)
    f[0] = omega1 + K1*np.sin(theta[1]-theta[0])
    f[1] = omega2 + K2*np.sin(theta[0]-theta[1])
    return(f)


def euler(dt, tf, theta0, gradV, x1, x2, omega1, omega2, K1, K2,rate):
    T = np.int32(tf/dt)
    thetaout = np.zeros((2,T))
    thetaout[:,0] = theta0
    dN1 = sim_poisson(2,dt,tf,rate)
    dN2 = sim_poisson(2,dt,tf,rate)
    for i in range(0, T-1):
        thetat = thetaout[:,i]
        #print(thetat)
        u = np.zeros(2)
        # u[0] = -sp.interpolate.interpn((x1,x2),gradV[0,:,:,i],thetat, 
        #                                bounds_error=False, fill_value=None)
        # u[1] = -sp.interpolate.interpn((x1,x2),gradV[1,:,:,i],thetat, 
        #                                bounds_error=False, fill_value=None)
        fout = f(thetat, omega1, omega2, K1, K2)
        thetanew = thetat + fout*dt + u*dt + dN1[:,i] - dN2[:,i]
        thetaout[:, i+1] = np.mod(thetanew, 2*pi)
    return(thetaout)
###################################################################
#
#
# please put your file location here if you want to
# compute an optimal control from an HJB solution!
#
###################################################################

# fn = 'FILE LOCATION HERE'
# filen = 'simDataHJBcosine.hdf5'
# f1 = h5.File(fn + filen, 'r')
# gradV = f1['/']['gradV'][()]
# theta1 = f1['/']['theta1'][()]
# theta2 = f1['/']['theta2'][()]
gradV = 0
theta1 = 0
theta2 = 0
dt = 5e-4
tf = 5
theta0 = np.zeros(2)
theta0[0] = np.mod(sps.vonmises.rvs(1,loc=0) + pi, 2*pi)
theta0[1] = np.mod(sps.vonmises.rvs(1,loc=0) + pi, 2*pi)
###################################################################
#
#
# make sure you match your parameters between the HJB and 
# SDE so your control is optimal!
#
##################################################################
omega1 = 1
omega2 = 1
K1 = 1
K2 = 1
rate = .5
thetaout = euler(dt, tf, theta0, gradV, theta1, theta2, omega1, omega2, K1, K2, rate)
#
# comment the line below out if you don't have latex!
#
plt.rcParams['text.usetex'] = True
fig = plt.figure(figsize=(10, 4))
ax1 = fig.add_subplot(121)
t = np.linspace(0, tf, num = np.int32(tf/dt))
plt.plot(thetaout[0,:].T,thetaout[1,:].T,'.')
plt.xlabel('$\\theta^1_t$ (radians)', usetex=True)
plt.ylabel('$\\theta^2_t$ (radians)', usetex=True)
plt.title('Optimal Trajectory in State Space', usetex=True)
plt.xlim(0,2*pi)
plt.ylim(0,2*pi)
ax1 = fig.add_subplot(122)
t = np.linspace(0, tf, num = np.int32(tf/dt))
plt.plot(t,thetaout[:,:].T,'.',markersize=2)
plt.xlabel('$t$ (arb. units)', usetex=True)
plt.ylabel('$\\theta_t^i$ (radians)', usetex=True)
plt.title('Optimal Trajectory in Time', usetex=True)
plt.xlim(0,5)
plt.ylim(0,2*pi)