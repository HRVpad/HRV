from loadData import sleeper
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np

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