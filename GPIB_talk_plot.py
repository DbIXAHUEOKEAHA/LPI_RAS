# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 18:34:12 2021

@author: user
"""

import pyvisa as visa
import time
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

#Check if everything connected properly
rm = visa.ResourceManager()
rm.list_resources()

print(rm.list_resources(), '\n')

#Setting devices names
lock_in = rm.open_resource('GPIB0::1::INSTR', write_termination= '\n', read_termination='\n')
keyt2000 = rm.open_resource('GPIB0::2::INSTR', write_termination= '\n', read_termination='\n')
keyt2010 = rm.open_resource('GPIB0::3::INSTR', write_termination= '\n', read_termination='\n')

#Write command to a device and get it's output
def get(device, command):
    device.write(command)
    return device.read()

print(get(lock_in, 'OUTP? 3'))
'''
#setting matplotlib parameters
plt.rcParams['animation.html'] = 'jshtml'
fig = plt.figure(figsize = (5,5), dpi = 100)
ax = fig.add_subplot(111)

#forming data into file
zero_time = time.process_time()
data = pd.DataFrame(columns = ['Time', 'X_lock', 'Y_lock', 'V_keyt2000', 'V_keyt2010'], dtype = np.float)

filename = 'test_' + datetime.today().strftime('%H_%M_%d_%m_%Y') + '.csv'

print(filename, '\n')

#getting data
while True:
    cur_time = time.process_time() - zero_time
    
    data = data.append({'Time': cur_time, 'X_lock': get(lock_in, 'X.'), 'Y_lock': get(lock_in, 'Y.'), 'V_keyt2000': get(keyt2000, 'FETC?'), 'V_keyt2010': get(keyt2010, 'FETC?')}, ignore_index = True)
    data.to_csv(filename, sep = ' ')
    
    #Plotting data
    x = get(keyt2000, 'FETC?')
    y = get(lock_in, 'X.')
    
    print(x, y)
    
    ax.plot(np.float(x),  np.float(y), '*-', color = 'blue')
    ax.grid()
    fig.show()
    fig.canvas.draw()
    
    time.sleep(0.1)
'''
