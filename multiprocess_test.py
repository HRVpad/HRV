# Testing multiprocessing
from multiprocessing import Process, Value, Manager
import numpy as np
import time
import sys
import os

# Will attempt to import pyqtgraph if not then will install then import
try:
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtGui, QtCore
except:
    from pip._internal import main
    main(['install', 'pyqtgraph'])
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtGui, QtCore
   ## os.system('python multiprocess_test.py')


# a1, a2 = [0, 0 ,0], []
def sleeper(s):
    """
    ==========================================================================
    Function - Parameter
    ==========================================================================
    * Pauses the function for **s** seconds.
    """
    
    end = time.time_ns() + s*1E9
    while time.time_ns()<end:
       pass

    
def loadData(dataDir):
    """
    ==========================================================================
    Function - Parameter
    ==========================================================================
    * Loads the **dataDir**.csv file.
    """
    lst = []                                # empty list to append preloaded data 
    with open(dataDir) as f:
        for line in f: # loads each sample
            lst += line.split() 
    
    lst.pop(0); lst.pop(0)
    
    ecg = []
    for l in lst:
        ecg.append(float(l.split(',')[1]))
        
    return ecg
        
#    while lst[0].replace(',', '').isnumeric() == False:
#        lst.pop(0)                          # removes the non numerical indices
#                                            # only works for csv with comma as delimeter
#    else:
#        pass
#    
#    master = []
#    for l in range(lst[0].count(',')):
#        command = 'list' + str(l+1) + '= []'
#        exec(command)
#        for sample in range(len(lst)):
#            command = 'list' + str(l+1) + '.append(float(lst[' + str(sample) + '].split(' + '","' + ')[' + str(l+1) + ']))'
#            exec(command)
#        command = 'master.append(list' + str(l+1) + ')'
#        exec(command)
#    return master
            
        

def signal(a1, sample_freq, runtime, sig): 
    endtime = time.time() + runtime.value
    t = 0
    while time.time()<endtime:
        sample_time = t/sample_freq.value   # sample time = sample index / sample frequency
        #a = np.sin(4*np.pi*sample_time)     # sinusoid signal capture
        a = sig[t]
        t += 1                              # next sample
        a1.append(a + 50*np.random.rand())     # append the signal value
        sleeper(1/sample_freq.value)        # controlling the loop iteration time with the sampling frequency
        #print(a)
        #end = time.time()
        #sample_rate = end - start
        #if time.time()>endtime:             # run the loop for given time
         #   break 
    #return a1


def liveFilter(a1, a2, sample_freq):
    fil1 = [0.1, 0.2, 0.7, 0.8, 0.7, 0.6, 0.5] # FIR moving average
    #fil2 = [1, 0.9, 0.8]  # for IIR
    while True:
        sleeper(1/sample_freq.value)
        a = np.dot(fil1,a1[-7:])/np.sum(fil1)
        #a -= np.dot(fil2,a2[-3:])
        a2.append(a)
        if len(a2) == len(a1)-7:
            break


# Realtime data plot. Each time this function is called, the data display is updated
def update(app, curve1, curve2, ptr, Xecg, Xppg, a1, a2):
    #global curve1, curve2, ptr, Xm    
    Xecg[:-1] = Xecg[1:]                  # shift data in the temporal mean 1 sample left
    Xppg[:-1] = Xppg[1:]
    #value = ser.readline()                # read line (single value) from the serial port
    Xecg[-1] = float(a1[-1])               # vector containing the instantaneous values 
    Xppg[-1] = float(a2[-1])     
    ptr += 1                              # update x position for displaying the curve
    #Xecg[:-1] = Xecg[1:]                  # shift data in the temporal mean 1 sample left
    #Xppg[:-1] = Xppg[1:]
    #value = ser.readline()                # read line (single value) from the serial port
    #Xecg[-1] = float(a1[-1])               # vector containing the instantaneous values      
    #Xppg[-1] = float(a2[-2])
    #ptr += 1                              # update x position for displaying the curve
    curve1.setData(Xecg)                  # set the curve .with this data
    curve1.setPos(ptr,0)                  # set x position in the graph to 0
    curve2.setData(Xppg)
    curve2.setPos(ptr,0)
    app.processEvents()    # you MUST process the plot now

def run_graph(a1, a2, sample_freq):
    ### START QtApp #####
    app = QtGui.QApplication([])            # you MUST do this once (initialize things)
    ####################

    win = pg.GraphicsWindow(title="Sinusoid") # creates a window
    win.show()
    p = win.addPlot(1,1, title="Raw")  # creates empty space for the plot in the window
    k = win.addPlot(2,1, title="Filter")
    curve1 = p.plot()                        # create an empty "plot" (a curve to plot)
    curve2 = k.plot()


    windowWidth = 500                       # width of the window displaying the curve
    Xecg = np.linspace(0,0,windowWidth)        # create array that will contain the relevant time series 
    Xppg = np.linspace(0,0,windowWidth)        # create array that will contain the relevant time series    
    ptr = -windowWidth                      # set first x position
    while True:
        update(app, curve1, curve2, ptr, Xecg, Xppg, a1, a2)
        sleeper(1/sample_freq.value)
    
    ### END QtApp ####
    #QtGui.QApplication.exec_() # you MUST put this at the end
    QtGui.QApplication.instance().exec_()
    app.quit()
    ##################


# Variables

a1 = [0,0,0,0,0,0,0]
a2 = []

if __name__ == '__main__':
    with Manager() as manager:
        sample_freq = Value('i', 750)
        b = Value('d',0)
        runtime = Value('d',60)
        #a1 = Array('d',[0, 0, 0])
        #a2 = Array('d', [])
        a1 = manager.list([0,0,0,0,0,0,0])
        a2 = manager.list()
        sig = loadData('100.csv')
        #sig = sig[0]
        
        # Parallel process set up
        p = Process(target=signal, args=(a1, sample_freq, runtime, sig,))
        c = Process(target=liveFilter, args=(a1, a2, sample_freq,))
        g = Process(target=run_graph, args=(a1, a2, sample_freq,))
        g.daemon = False
        
        # Parallel process start
        p.start()
        c.start()
        g.start()
        
        # Waits till all processes are finished
        p.join()
        c.join()
        g.kill()

        # Acquired list of data that can be further developed
        a1 = list(a1) # raw data
        a2 = list(a2) # filtered data

