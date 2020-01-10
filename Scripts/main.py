# Testing
from multiprocessing import Process, Value, Manager 
from loadData import *
from livePlot import run_graph
import sys
import os


if __name__ == '__main__':
    with Manager() as manager:

        # Arduino variables:
        portName = 'COM3'                       # list the com port from arduino IDE
        baudrate = 19600                        # Have it high enough so that way python sampling rate could pick up

        # Directory location for preloaded data:
        directory = '../Data/100.csv'

        # Sampling and recording variables:
        sample_freq = Value('i', 361)          
        b = Value('d',0)
        runtime = Value('d',60)                 # Runs for 30 seconds

        # Filter variables: extra zeros are for padding in filter
        a1 = manager.list([0,0,0,0,0,0,0,0,0,0,0,0,0])
        a2 = manager.list([0,0,0,0,0,0,0])

        # Specifying where the signal is coming from
        #sig = arduino(portName, baudrate)       # For arduino live signal
        sig = csv(directory)             # For preloaded data

        
        # Parallel process set up
        p = Process(target=signal, args=(a1, sample_freq, runtime, sig,))
        c = Process(target=filter, args=(a1, a2, sample_freq,))
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
