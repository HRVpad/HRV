# Testing
from multiprocessing import Process, Value, Manager
from HRV import *
from loadData import *
from livePlot import run_graph
import sys
import os
import matplotlib

matplotlib.use('TkAgg')
plt = matplotlib.pyplot


if __name__ == '__main__':
    with Manager() as manager:

        # Arduino variables:
        portName = 'COM3'                       # list the com port from arduino IDE
        baudrate = 9600                        # Have it high enough so that way python sampling rate could pick up

        # Directory location for preloaded data:
        ecgDir = '../Data/100.csv'
        ppgDir = '../Data/SampleGSRPPG_Session1_Shimmer_B640_Calibrated_SD.csv'

        # Sampling and recording variables:
        sample_freq_ecg = Value('i', 360)
        sample_freq_ppg = Value('i', 128)          
        b = Value('d',0)
        runtime = Value('d',60)                 # Runs for 30 seconds

        # Filter variables: extra zeros are for padding in filter
        a1 = manager.list([0,0,0,0,0,0,0,0,0,0,0,0,0])
        a2 = manager.list([0,0,0,0,0,0,0])
        a3 = manager.list([0,0,0,0,0,0,0,0,0,0,0,0,0])
        a4 = manager.list([0,0,0,0,0,0,0])
        delT_ECG = manager.list([])
        delT_PPG = manager.list([])

        # Specifying where the signal is coming from
        #sig = arduino(portName, baudrate)       # For arduino live signal
        ecg = csv_ecg(ecgDir)             # For preloaded data
        ppg = csv_ppg(ppgDir)

        
        # Parallel process set up
        p = Process(target=signal_ecg, args=(a1, sample_freq_ecg, runtime, ecg, delT_ECG))
        c = Process(target=filter_ecg, args=(a1, a2, sample_freq_ecg,))
        q = Process(target=signal_ppg, args=(a3, sample_freq_ppg, runtime, ppg, delT_PPG))
        m = Process(target=filter_ppg, args=(a3, a4, sample_freq_ppg,))
        g = Process(target=run_graph, args=(a1, a2, a3, a4, sample_freq_ppg,))
        g.daemon = False
        
        # Parallel process start
        p.start()
        c.start()
        q.start()
        m.start()
        g.start()
        
        # Waits till all processes are finished
        p.join()
        c.join()
        g.kill()

        # Acquired list of data that can be further developed
        a1 = list(a1) # raw data
        a2 = list(a2) # filtered data
        delT_ECG = list(delT_ECG)
        delT_PPG = list(delT_PPG)

        print('Average Sampling Rate is '+str(len(a1)/60))

        #freqDomain = HRV1(a2, sample_freq_ecg)
        plt.figure()
        plt.plot(delT_ECG); plt.xlabel('Sample'); plt.ylabel('Sampling Rate (Hz)'); plt.show()
        plt.title('Sampling Rate Per Sample')

