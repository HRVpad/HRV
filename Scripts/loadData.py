import time
def sleeper(s):
    """
    
    Function - Parameter
    ==========================================================================
    * Pauses the function for **s** seconds.
    
    """
    
    end = time.perf_counter() + s
    while time.perf_counter()<end:
       pass


def csv(dataDir):
    """
    Function - Parameter
    ==========================================================================
    * Loads the **dataDir**.csv file.
    
    Note: this function only works for data obtained from kaggler
    """
    lst = []                                # empty list to append preloaded data 
    with open(dataDir) as f:
        for line in f:                      # loads each sample
            lst += line.split() 
    
    lst.pop(0); lst.pop(0)
    
    ecg = []
    for l in lst:
        ecg.append(float(l.split(',')[1]))
        
    return ecg


def arduino(portName,baudrate):
    """
    Function - Parameter
    ==========================================================================
    * Loads arduino serial from **portName**.
    * **baudrate** specifies the connection between arduino and computer

    Note: baudrate must be set on the arduino ide prior to executing this function
    """        

    import serial
    ser = serial.Serial(portName,baudrate)
    return ser



def signal(a1, sample_freq, runtime, sig):
    import time
    endtime = time.perf_counter() + runtime.value
    t = 0
    if len(sig) > 1:                            # if sig is a vector
        while time.perf_counter()<=endtime:
            a = sig[t]
            t += 1                              # next sample
            a1.append(a)                        # append the signal value
            sleeper(1/sample_freq.value)        # controlling the loop iteration time with the sampling frequency
    else:
        while time.perf_counter()<=endtime:
            a = sig
            t += 1                              # next sample
            a1.append(a)                        # append the signal value
            sleeper(1/sample_freq.value)        # controlling the loop iteration time with the sampling frequency

def filter(a1, a2, sample_freq):
    from scipy import signal as sc
    import numpy as np

    #fil1 = [0.1, 0.2, 0.7, 0.8, 0.7, 0.6, 0.5] # FIR moving average
    fil1 = sc.firwin(7, [0.05, 25, 49, 50], fs=360, pass_zero=False)
    #c, d = sc.iirfilter(1, [0.5, 50], btype='band', rs=60, analog=False, ftype='cheby2', fs=360)
    d = np.array([1, -0.7, 0.98, -0.2, 0.8, 0.4, 0.6]) # for IIR
    while True:
        sleeper(1/sample_freq.value)
        a = np.dot(fil1,a1[-7:])/sum(abs(fil1))
        a += np.dot(d[1:],a2[-6:])/sum(abs(d))
        a2.append(a)
        if len(a2) == len(a1)-7:
            break


    
