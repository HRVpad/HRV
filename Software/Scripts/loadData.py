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


def csv_ecg(dataDir):
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

def csv_ppg(dataDir):
    """
    Function - Parameter
    ==========================================================================
    * Loads the **dataDir**.csv file.
    
    Note: this function only works for data obtained from shimmersensing
    """
    lst = []                                # empty list to append preloaded data 
    with open(dataDir) as f:
        for line in f:                      # loads each sample
            lst += line.split(' ') 
    
    lst.pop(0); lst.pop(0); lst.pop(0); lst.pop(0); lst.pop(0)
    
    ppg = []
    for l in range(0,len(lst),2):
        ppg.append(float(lst[l].split('\t')[6]))
        
    return ppg



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



def signal_ecg(a1, sample_freq, runtime, sig, delT):
    import time
    endtime = time.perf_counter() + runtime.value
    t = 0
    if len(sig) > 1:                            # if sig is a vector
        import numpy as np
        while time.perf_counter()<=endtime:
            start = time.perf_counter()
            a = sig[t] + 400*(np.sin(120*np.pi*t) + np.cos(60*np.pi*t)) + 200*np.random.rand()
            t += 1                              # next sample
            a1.append(a)                        # append the signal value
            end = time.perf_counter()
            codeTime = end - start
            sleeper(1/(sample_freq.value + 2*codeTime))        # controlling the loop iteration time with the sampling frequency
            delT.append(1/(time.perf_counter()-start))
    else:
        while time.perf_counter()<=endtime:
            sig = arduino('COM3',9600)
            start = time.perf_counter()
            a = sig
            t += 1                              # next sample
            a1.append(a)                        # append the signal value
            end = time.perf_counter()
            codeTime = end - start
            sleeper(1/sample_freq.value)        # controlling the loop iteration time with the sampling frequency

def filter_ecg(a1, a2, sample_freq):
    from scipy import signal as sc
    import numpy as np

    #fil1 = [0.1, 0.2, 0.7, 0.8, 0.7, 0.6, 0.5] # FIR moving average
    fil1 = sc.firwin(170, [1, 25, 49, 50], fs=360, pass_zero=False)
    #c, d = sc.iirfilter(1, [0.5, 50], btype='band', rs=60, analog=False, ftype='cheby2', fs=360)
    d = np.array([1, -0.3, 0.98, -0.1, 0.85, 0.4, 0.6]) # for IIR
    while True:
        sleeper(1/sample_freq.value)
        a = np.dot(fil1,a1[-170:])/sum(abs(fil1))
        a += np.dot(d[1:],a2[-6:])/sum(abs(d))
        a2.append(a)
        if len(a2) == len(a1)-7:
            break

def signal_ppg(a3, sample_freq_ppg, runtime, sig, delT):
    import time
    endtime = time.perf_counter() + runtime.value
    t = 0
    if len(sig) > 1:                            # if sig is a vector
        import numpy as np
        while time.perf_counter()<=endtime:
            start = time.perf_counter()
            t += 1                              # next sample
            ab = sig[t] + 800*np.random.rand()
            a3.append(ab)                        # append the signal value
            end = time.perf_counter()
            codeTime = end - start
            sleeper(1/(sample_freq_ppg.value + 2*codeTime))        # controlling the loop iteration time with the sampling frequency
            delT.append(time.perf_counter()-start)
    else:
        while time.perf_counter()<=endtime:
            start = time.perf_counter()
            ab = sig
            t += 1                              # next sample
            a1.append(ab)                        # append the signal value
            end = time.perf_counter()
            codeTime = end - start
            sleeper(1/sample_freq_ppg.value)        # controlling the loop iteration time with the sampling frequency

def filter_ppg(a3, a4, sample_freq_ppg):
    from scipy import signal as sc
    import numpy as np

    #fil1 = [0.1, 0.2, 0.7, 0.8, 0.7, 0.6, 0.5] # FIR moving average
    fil1 = sc.firwin(20, [1, 3], fs=128, pass_zero=False)
    #c, d = sc.iirfilter(1, [0.5, 50], btype='band', rs=60, analog=False, ftype='cheby2', fs=360)
    d = np.array([1, 0.2, 0.98, -0.05, 0.85, 0.5, 0.6]) # for IIR
    while True:
        sleeper(1/sample_freq_ppg.value)
        a = np.dot(fil1,a3[-20:])/sum(abs(fil1))
        a += np.dot(d[1:],a4[-6:])/sum(abs(d))
        a4.append(a)
        if len(a4) == len(a3)-7:
            break

