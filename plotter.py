# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 20:05:45 2021

@author: user
"""

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

filename = 'raman_17_45_01_05_2021'

data = pd.read_csv((filename + '.csv'), sep = ' ')

def f(x, a, b):
    return a * x + b

def lsq():
    calibration = pd.read_csv('calibration.csv', sep = ' ')
    
    #p0=np.array([])
    
    beta_opt, beta_cov = optimize.curve_fit(f, calibration['R_keyt2000'], calibration['lambda'])
    #beta_perr = np.sqrt(np.diag(beta_cov))
    
    return beta_opt

def wavelen2rgb(nm):
    """
    Converts a wavelength between 380 and 780 nm to an RGB color tuple.
    Argument:
        nm: Wavelength in nanometers.
    Returns:
        a 3-tuple (red, green, blue) of integers in the range 0-255.
    """

    def adjust(color, factor):
        if color < 0.01:
            return 0
        max_intensity = 255
        gamma = 0.80
        rv = int(round(max_intensity * (color * factor)**gamma))
        if rv < 0:
            return 0
        if rv > max_intensity:
            return max_intensity
        return rv

    if nm < 380 or nm > 780:
        return "#000000"
    red = 0.0
    green = 0.0
    blue = 0.0
    # Calculate intensities in the different wavelength bands.
    if nm < 440:
        red = -(nm - 440.0) / (440.0 - 380.0)
        blue = 1.0
    elif nm < 490:
        green = (nm - 440.0) / (490.0 - 440.0)
        blue = 1.0
    elif nm < 510:
        green = 1.0
        blue = -(nm - 510.0) / (510.0 - 490.0)
    elif nm < 580:
        red = (nm - 510.0) / (580.0 - 510.0)
        green = 1.0
    elif nm < 645:
        red = 1.0
        green = -(nm - 645.0) / (645.0 - 580.0)
    else:
        red = 1.0
    # Let the intensity fall off near the vision limits.
    if nm < 420:
        factor = 0.3 + 0.7 * (nm - 380.0) / (420.0 - 380.0)
    elif nm < 701:
        factor = 1.0
    else:
        factor = 0.3 + 0.7 * (780.0 - nm) / (780.0 - 700.0)
    # Return the calculated values in an (R,G,B) tuple.
    return "#{0:02x}{1:02x}{2:02x}".format(int(adjust(red, factor)), int(adjust(green, factor)), adjust((blue, factor)))

def plot(x, y, filename):
    plt.figure()
    plt.plot(x, y, 'o', label = r'$I(\lambda)$')
    plt.legend()
    plt.grid()
    plt.title(('Спектр'))
    plt.xlabel(r'$\lambda$, nm')
    plt.ylabel('Intensity, abs')
    plt.savefig(filename + '.png', dpi = 300)
    
plot(data['R_keyt2000'].values * lsq()[0] + lsq()[1], data['X_lock'].values, filename)