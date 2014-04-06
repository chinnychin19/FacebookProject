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
k=1.0

TS=1.0
ND=70.0
I0=1-1e-6
S0=1e-6
INPUT = (I0, S0, 0.0)


def diff_eqs(INP,t):  
	'''The main set of equations'''
	Y=np.zeros((3))
	V = INP    
	Y[0] = - lambd * k * V[0] * V[1]
	Y[1] = lambd * k * V[0] * V[1] - alpha * k * V[1] * ( V[1] + V[2] )
	Y[2] = alpha * k * V[1] * (V[1] + V[2] )
	return Y   # For odeint

t_start = 0.0; t_end = ND; t_inc = TS
t_range = np.arange(t_start, t_end+t_inc, t_inc)
RES = spi.odeint(diff_eqs,INPUT,t_range)

print RES

#Ploting
pl.subplot(211)
pl.plot(RES[:,0], '-g', label='Ignorants')
pl.plot(RES[:,2], '-k', label='Stiflers')
pl.legend(loc=0)
pl.title('SIR')
pl.xlabel('Time')
pl.ylabel('Ignorants and Stiflers')
pl.subplot(212)
pl.plot(RES[:,1], '-r', label='Spreaders')
pl.xlabel('Time')
pl.ylabel('Spreaders')
pl.savefig('rumor-sir.png')

