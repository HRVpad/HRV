import numpy as np
import pyhrv
import biosppy
import pyhrv.tools as tools
import pyhrv.frequency_domain as fd
import hrvanalysis
import matplotlib.pyplot as plt

def HRV1(a2, sample_freq):
   rpeaks = biosppy.signals.ecg.ecg(signal=a2, sampling_rate=sample_freq.value)[2]
   #NNi = tools.nn_intervals(rpeaks)

   result = fd.ar_psd(rpeaks=rpeaks)


def HRV2(a2, sample_freq):
    sec2msec = 1000
    rpeaks = biosppy.signals.ecg.ecg(signal=a2, sampling_rate=sample_freq.value)[2]
    RRi = np.diff(rpeaks)*sec2msec/sample_freq.value
    NNi = hrvanalysis.remove_outliers(rr_intervals=RRi, low_rri=300, high_rri=2000)
    NNi = hrvanalysis.interpolate_nan_values(rr_intervals=NNi, interpolation_method="linear")
    NNi = hrvanalysis.remove_ectopic_beats(rr_intervals=NNi, method='malik')
    NNi = hrvanalysis.interpolate_nan_values(rr_intervals=NNi, interpolation_method="linear")
    freq_domain = hrvanalysis.extract_features.get_frequency_domain_features(NNi, method='lomb')
    
    print(freq_domain)
    hrvanalysis.plot_psd(NNi, method="lomb")

def ppg_summary(a4, sample_freq):
   rpeaks = biosppy.signals.bvp.bvp(signal=a2, sampling_rate=sample_freq.value)[2]



    
    
