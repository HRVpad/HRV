from loadData import sleeper
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

# Realtime data plot. Each time this function is called, the data display is updated
def update(app, curve1, curve2, curve3, curve4, ptr, Xecg_raw, Xecg_fil, Xppg_raw, Xppg_fil, a1, a2, a3, a4):
    #global curve1, curve2, ptr, Xm    
    Xecg_raw[:-1] = Xecg_raw[1:]                  # shift data in the temporal mean 1 sample left
    Xecg_fil[:-1] = Xecg_fil[1:]
    Xppg_raw[:-1] = Xppg_raw[1:]
    Xppg_fil[:-1] = Xppg_fil[1:]
    #value = ser.readline()                # read line (single value) from the serial port
    Xecg_raw[-1] = float(a1[-1])               # vector containing the instantaneous values 
    Xecg_fil[-1] = float(a2[-1]) 
    Xppg_raw[-1] = float(a3[-1])
    Xppg_fil[-1] = float(a4[-1])    
    ptr += 1                              # update x position for displaying the curve
    #Xecg[:-1] = Xecg[1:]                  # shift data in the temporal mean 1 sample left
    #Xppg[:-1] = Xppg[1:]
    #value = ser.readline()                # read line (single value) from the serial port
    #Xecg[-1] = float(a1[-1])               # vector containing the instantaneous values      
    #Xppg[-1] = float(a2[-2])
    #ptr += 1                              # update x position for displaying the curve
    curve1.setData(Xecg_raw)                  # set the curve .with this data
    curve1.setPos(ptr,0)                  # set x position in the graph to 0
    curve2.setData(Xecg_fil)
    curve2.setPos(ptr,0)
    curve3.setData(Xppg_raw)                  # set the curve .with this data
    curve3.setPos(ptr,0)                  # set x position in the graph to 0
    curve4.setData(Xppg_fil)
    curve4.setPos(ptr,0)
    app.processEvents()    # you MUST process the plot now

def run_graph(a1, a2, a3, a4, sample_freq):
    ### START QtApp #####
    app = QtGui.QApplication([])            # you MUST do this once (initialize things)
    ####################

    win = pg.GraphicsWindow(title="ECG Signal") # creates a window
    win.show()
    p = win.addPlot(1,1, title="Raw ECG")  # creates empty space for the plot in the window
    k = win.addPlot(2,1, title="Filtered ECG")
    l = win.addPlot(3,1, title="Raw PPG")  # creates empty space for the plot in the window
    m = win.addPlot(4,1, title="Filtered PPG")
    curve1 = p.plot()                        # create an empty "plot" (a curve to plot)
    curve2 = k.plot()
    curve3 = l.plot()                        # create an empty "plot" (a curve to plot)
    curve4 = m.plot()



    windowWidth = 500                                            # width of the window displaying the curve
    Xecg_raw = np.linspace(0,0,windowWidth)        # create array that will contain the relevant time series 
    Xecg_fil = np.linspace(0,0,windowWidth)        # create array that will contain the relevant time series
    Xppg_raw = np.linspace(0,0,windowWidth)        # create array that will contain the relevant time series 
    Xppg_fil = np.linspace(0,0,windowWidth)        # create array that will contain the relevant time series    
    ptr = -windowWidth                         # set first x position
    while True:
        update(app, curve1, curve2, curve3, curve4, ptr, Xecg_raw, Xecg_fil, Xppg_raw, Xppg_fil, a1, a2, a3, a4)
        sleeper(1/sample_freq.value)
    
    ### END QtApp ####
    #QtGui.QApplication.exec_() # you MUST put this at the end
    QtGui.QApplication.instance().exec_()
    app.quit()
    ##################