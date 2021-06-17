# -*- coding: utf-8 -*-
"""
Created on Tue May  4 18:36:40 2021

@author: user
"""
import serial

ser = serial.Serial()
ser.timeout = 0.3
ser.port = "com3"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_EVEN
ser.stopbits = serial.STOPBITS_ONE
ser.open()

ser.write(b'SD10*')
print(ser.read(10))
ser.write(b'MV10*')
print(ser.read(10))
ser.close()