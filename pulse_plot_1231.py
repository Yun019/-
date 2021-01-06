import matplotlib.pyplot as plt
import numpy as np
import time
import time, random
import math
import serial
from collections import deque
from scipy import signal


#Display loading 
class PlotData:
    def __init__(self, max_entries=30):
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y = deque(maxlen=max_entries)
        self.x=np.linspace(0, 100, 500)
    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y.append(y)
     


#initial
fig, (ax,ax2,ax3,ax4) = plt.subplots(4,1)
line,  = ax.plot(np.random.randn(100))
line2, = ax2.plot(np.random.randn(100))
line3, = ax3.plot(np.random.randn(100))
line4, = ax4.plot(np.random.randn(100))
plt.show(block = False)
plt.setp(line2,color = 'r')




PData= PlotData(500)
PData2= PlotData(500)
ax.set_ylim(0, 500)
ax2.set_ylim(-20, 20)
ax3.set_ylim(0,500)
ax4.set_ylim(-20, 20)


# plot parameters
print ('plotting data...')
# open serial port
strPort='com3'
ser = serial.Serial(strPort, 115200)
ser.flush()

start = time.time()



while True:
    
    for ii in range(10):

        try:
            data = float(ser.readline())
            PData.add(time.time() - start, data)
        except:
            pass
    
    xf = np.fft.fft(PData.axis_y)
    xf2=xf
    xf2[0] = 0
    xf2 = np.fft.ifft(xf2)
    xf3 = signal.lfilter([1/3, 1/3, 1/3], 1, xf2)
    
    
    ax.set_xlim(PData.axis_x[0], (PData.axis_x[0]+5))
    ax2.set_xlim(PData.axis_x[0], (PData.axis_x[0]+5))
    ax3.set_xlim(0,100)
    ax4.set_xlim(PData.axis_x[0], (PData.axis_x[0]+5))

    line.set_xdata(PData.axis_x)
    line.set_ydata(PData.axis_y)
    line2.set_xdata(PData.axis_x)
    line2.set_ydata(xf2)
    
    if len(xf)==500:
        line3.set_xdata(PData.x)
        line3.set_ydata(abs(xf))

    line4.set_xdata(PData.axis_x)
    line4.set_ydata(xf3)
    print(len(xf))
    fig.canvas.draw()
    fig.canvas.flush_events()
