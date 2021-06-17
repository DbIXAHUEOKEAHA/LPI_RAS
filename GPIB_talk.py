# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pyvisa as visa
import time
from datetime import datetime
import numpy as np
import pandas as pd

#Check if everything connected properly
rm = visa.ResourceManager()
rm.list_resources()

print(rm.list_resources(), '\n')

#Setting devices names
lock_in = rm.open_resource('GPIB0::1::INSTR', write_termination= '\n')
keyt2000 = rm.open_resource('GPIB0::2::INSTR', write_termination= '\n', read_termination='\n')
keyt2010 = rm.open_resource('GPIB0::3::INSTR', write_termination= '\n', read_termination='\n')

#Write command to a device and get it's output
def get(device, command):
    device.write(command)
    return device.read()

print(get(lock_in, 'DDEF?11'))
    
