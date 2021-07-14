import pyvisa as visa
import time
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
plt.rcParams['animation.html'] = 'jshtml'
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.animation as animation
import tkinter as tk
from tkinter import ttk
from scipy import optimize
import serial

ser = serial.Serial()
ser.timeout = 0.3
ser.port = "com3"
ser.baudrate = 9600
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_EVEN
ser.stopbits = serial.STOPBITS_ONE
ser.open()
#ser.write(b'ST1*')

LARGE_FONT = ('Verdana', 12)
style.use('ggplot')

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

def f(x, a, b):
    return a * x + b

def lsq():
    calibration = pd.read_csv(r'C:\Users\user\Desktop\Kravtsov\spectrum\calibration.csv', sep = ' ')
    
    #p0=np.array([])
    
    beta_opt, beta_cov = optimize.curve_fit(f, calibration['R_keyt2000'], calibration['lambda'])
    #beta_perr = np.sqrt(np.diag(beta_cov))
    
    return beta_opt

a = lsq()[0]
b = lsq()[1]

#forming data into file
zero_time = time.process_time()
data = pd.DataFrame(columns = ['Time', 'lock_in', 'R_keyt2000', 'V_keyt2010'], dtype = np.float)

filename = r'C:\Users\user\Desktop\Kravtsov\spectrum\one_more_try_' + datetime.today().strftime('%H_%M_%d_%m_%Y') + '.csv'

print(filename, '\n')

fig = Figure(figsize = (5, 5), dpi = 200)
ax = fig.add_subplot(111)

def animate(i):
    
    global data
    global a
    global b
    
    cur_time = time.process_time() - zero_time
    
    data = data.append({'Time': cur_time, 'lock_in': get(lock_in, 'OUTP? 3'), 'R_keyt2000': get(keyt2000, 'FETC?'), 'V_keyt2010': get(keyt2010, 'FETC?')}, ignore_index = True)
    data.to_csv(filename, sep = ' ')
    
    #Plotting data
    y = np.float(get(lock_in, 'OUTP? 3'))
    x = np.float(get(keyt2000, 'FETC?'))
    if y == '0.0E+00\x00\r':
        y = 0
    else:
        y = np.float(y)
    
    ax.plot(x * a + b, y, '-o', color = 'blue')
    
    if moving_indicator == True:
        data = data.append({'Time': cur_time, 'lock': y, 'R_keyt2000': x, 'V_keyt2010': get(keyt2010, 'FETC?')}, ignore_index = True)
        data.to_csv(filename, sep = ' ')
    

class spectrometer(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.iconbitmap(self)
        tk.Tk.wm_title(self, 'spectrometer')
        
        container = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = 'True')
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        
        for F in (StartPage, Settings, Graph):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nsew')
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
        
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = 'Start Page', font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)
        
        button = ttk.Button(self, text = "Settings", command = lambda: controller.show_frame(Settings))
        button.pack()
        
        button2 = ttk.Button(self, text = 'Graph', command = lambda: controller.show_frame(Graph))
        button2.pack()
        
        
class Settings(tk.Frame):

    def __init__(self, parent, controller):
        
        global lock_in_speed
        global moving_indicator
        global starting_time
        
        moving_indicator = False
        
        def move_tapped():
            global moving_indicator
            global starting_time
            ser.write(b'MV*')
            print(ser.read(10))
            moving_indicator = True
            starting_time = time.process_time()
        
        def stop_tapped():
            global moving_indicator
            ser.write(b'SP*')
            print(ser.read(10))
            moving_indicator = False
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = 'Settings', font = LARGE_FONT)
        label.pack()
        
        button  = ttk.Button(self, text = 'Back to Home', command = lambda: controller.show_frame(StartPage))
        button.pack()
        
        mv_button = ttk.Button(self, text = 'Start moving', command = move_tapped)
        mv_button.place(relx = .8, rely = .4, anchor = 'c')
        
        rev_button = ttk.Button(self, text = 'Reverce', command = lambda: ser.write(b'RS*'))
        rev_button.place(relx = .8, rely = .43, anchor = 'c')
        
        stop_button = ttk.Button(self, text = 'Stop', command = stop_tapped)
        stop_button.place(relx = .8, rely = .46, anchor = 'c')
        
        lock_in_speed_label = tk.Label(self, text = r'Stepper speed steps/sec', font = LARGE_FONT)
        lock_in_speed_label.place(relx = .2, rely = .2, anchor = 'c')
        
        lock_in_speed = '200'
        lock_in_speed_entry = tk.Entry(self, textvariable = lock_in_speed)
        lock_in_speed_entry.place(relx = .2, rely = .23, anchor = 'c')
        
        save_button  = ttk.Button(self, text = 'Save', command = lambda: ser.write(str.encode('SD' + str(lock_in_speed_entry.get()) + '*')))
        ser.read(10)
        save_button.place(relx = .8, rely = .8, anchor = 'c')
        
class Graph(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = 'graph', font = LARGE_FONT)
        label.pack(pady = 10, padx = 10)
        
        button = ttk.Button(self, text = 'Back to Home', command = lambda: controller.show_frame(StartPage))
        button.pack()
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        
        '''
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side = tk.TOP, fill = tk.BOTH, expand = True)
        '''

def main():
    app = spectrometer()
    ani = animation.FuncAnimation(fig, animate, interval = 500)
    app.mainloop()
    ser.close()
    
if __name__ == '__main__':
    main()