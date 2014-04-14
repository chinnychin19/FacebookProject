#!/usr/bin/env python

# I = Ignorants
# S = Spreaders
# R = Stiflers
# lambd = transition rate from I to S
# alpha = transition rate from S to R
# k = percentage of population contact

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import scipy.integrate as spi
import numpy as np
import pylab as pl
lambd=1.4247
alpha=0.14286
delta=0.14286
k=1.0

TS=1.0
ND=70.0
N = 1
I0= N-1e-6
S0=1e-6
INPUT = (I0, S0)


Y=np.zeros((2))
def diff_eqs(INP,t):  
	'''The main set of equations'''
	Y=np.zeros((2))
	V = INP    
	Y[0] = - lambd * k * V[0] * V[1]
	Y[1] = lambd * k * V[0] * V[1] - alpha * k * V[1] * ( N - V[0] ) - delta * V[1]
	return Y   # For odeint

t_start = 0.0; t_end = ND; t_inc = TS
t_range = np.arange(t_start, t_end+t_inc, t_inc)
RES = spi.odeint(diff_eqs,INPUT,t_range)

# R = N - I - S
R = map(lambda x: N - x[0] - x[1], RES)

print RES
#Ploting
pl.subplot(211)
pl.plot(RES[:,0], '-g', label='Ignorants')
pl.plot(R, '-k', label='Stiflers')
pl.legend(loc=0)
pl.title('SIR')
pl.xlabel('Time')
pl.ylabel('Ignorants and Stiflers')
pl.subplot(212)
pl.plot(RES[:,1], '-r', label='Spreaders')
pl.xlabel('Time')
pl.ylabel('Spreaders')
pl.savefig('rumor-sir2.png')


###############################
# Phase Plane
###############################
def f(Y, t):
  y1, y2 = Y
  y1 = - lambd * k * Y[0] * Y[1]
  y2 = lambd * k * Y[0] * Y[1] - alpha * k * Y[1] * ( N - Y[0] ) - delta * Y[1]
  return [y1, y2]

  return [y2, -np.sin(y1)]
pl.figure()
y1 = np.linspace(0.0,1.0,20)
y2 = np.linspace(0.0,1.0,20)
Y1, Y2 = np.meshgrid(y1, y2)
t = 0

u, v = np.zeros(Y1.shape), np.zeros(Y2.shape)

NI, NJ = Y1.shape

for i in range(NI):
  for j in range(NJ):
    x = Y1[i, j]
    y = Y2[i, j]
    yprime = f([x, y], t)
    u[i,j] = yprime[0]
    v[i,j] = yprime[1]
Q = pl.quiver(Y1, Y2, u, v, color='r')

pl.xlabel('$Ignorants$')
pl.ylabel('$Spreaders$')
pl.xlim([0,1])
pl.ylim([0, 1])
pl.savefig('phase-portrait.png')

