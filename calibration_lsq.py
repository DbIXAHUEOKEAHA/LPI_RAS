# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 18:17:55 2019

@author: user
"""
import pandas as pd
import numpy as np
from scipy import optimize
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

def f(x, a, b):
    return a * x + b

data = pd.read_csv('calibration.csv', sep = ' ')

#p0=np.array([])

beta_opt, beta_cov = optimize.curve_fit(f, data['R_keyt2000'], data['lambda'])

print(beta_opt)

beta_perr = np.sqrt(np.diag(beta_cov))

plt.plot(data['R_keyt2000'], data['lambda'], '*', color = 'blue', label = 'data')
t = np.linspace(2700, 3500, 10000)
plt.plot(t, t * beta_opt[0] + beta_opt[1], '-', color = 'red', label = 'lsq')
plt.title(r'LSQ R -> $\lambda$')
plt.xlabel('R, Om')
plt.ylabel(r'$\lambda$, nm')
plt.savefig('lsq.png', dpi = 300)


