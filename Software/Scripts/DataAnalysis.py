# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 00:42:25 2020

@author: inkiy
"""

# import following modules
import numpy as np
import biosppy as bio # pip install biosppy
from datetime import datetime # pip install datetime
from matplotlib import pyplot as plt
from matplotlib import animation
from ecgdetectors import Detectors # pip install py-ecg-detectors
from scipy import signal
from scipy import stats
import csv
import pyhrv.frequency_domain as fd

num_subj = 3
num_trial = 3
subjects = ['Syed','Alain','Abel']
all_subj_data = {}
directory = 'Data/'
filtered_sticky_all = []
filtered_dry_all = []

for subj in range(num_subj):
	subj_sticky = np.empty(0) #Empty Array to append
	subj_dry = np.empty(0)
	statistics = []
	summary = [['Avg Sticky', 'Avg Dry', '% Deviation']]
	for trial in range(num_trial):
		data = [] # Empty set of data to be appended
		file = directory + 'Trial_' + str(trial+1) + '_' + subjects[0] + '.txt'
		with open(file) as datafile:
			for row in datafile:
				data.append(row.split()) # data appended in strong format
		
		# Processing data
		# Getting timelog of the data for sampling rate calculation and
		timelog = []
		sticky = []	
		dry = []	
		for l in range(700, len(data)-5000):
			try:
				minute = datetime.strptime(data[l][0], '%H:%M:%S.%f').minute
				second = datetime.strptime(data[l][0], '%H:%M:%S.%f').second
				totalsecond = minute*60 + second
				timelog.append(totalsecond)
				
				sticky.append([float(data[l][2]), float(data[l][3])])
				dry.append([-1*float(data[l][4]), -1*float(data[l][5])])
			except:
				pass
		
		# Histogram of samples per second	
		bins = len(np.argwhere(np.diff(timelog)>0)) # Separating bins by second
		#plt.hist(timelog, bins); plt.title('Samples per second')
		freq, binedge = np.histogram(timelog, bins) # Identifying frequency per bin
		SR = np.mean(freq) # Identifying sampling rate
		
		#info_sticky = bio.signals.ecg.ecg(signal=np.asarray(sticky)[:,1], sampling_rate=45, show=True)
		#info_dry = bio.signals.ecg.ecg(signal=np.asarray(dry)[:,1], sampling_rate=45, show=True)
		
		# Filter the signals for the RR peak detectors
		#b,a = signal.cheby1(2, 10, [0.5, 0.9], btype='bandpass', fs=SR, analog=False, output='ba')
		f = signal.firwin(11, [0.01, .8], pass_zero=False)
		#a = np.array([1, -0.5, 0.98])
		a = 1
		filtered_sticky = signal.lfilter(f,a,np.asarray(sticky)[500:,1])
		filtered_dry = signal.lfilter(f,a,np.asarray(dry)[500:,1])
		
		filtered_sticky_all.append(filtered_sticky)
		filtered_dry_all.append(filtered_dry)
		
		#plt.plot(filtered_dry)
		
		#filtered_sticky[filtered_sticky<0] = 0
		#filtered_dry[filtered_dry<0] = 0
		
		detectors = Detectors(SR) # specifying sampling rate for ECG
		rr_sticky = np.asarray(detectors.two_average_detector(filtered_sticky))
		rr_dry = np.asarray(detectors.two_average_detector(filtered_dry))
		
		
		# RR peak interval after hamilton RR peak detection
		delT_sticky = np.diff(rr_sticky)*1000/SR
		delT_dry = np.diff(rr_dry)*1000/SR
		
		# Mean delta t
		mean_sticky = np.mean(delT_sticky)
		mean_dry = np.mean(delT_dry)
		
		# Percent deviation calculation
		percent_dev = (100*abs(mean_sticky - mean_dry)/mean_sticky)
		
		# Mean delta t and percent deviation for each trial
		summary.append([mean_sticky, mean_dry, percent_dev])
		
		# Append all data for the subject
		subj_sticky = np.append(subj_sticky, delT_sticky)
		subj_dry = np.append(subj_dry, delT_dry)
		subj_electrode = [subj_sticky, subj_dry]
		
				
	statistics = (stats.ttest_ind(subj_electrode[0], subj_electrode[1], equal_var=False))
	all_subj_data[subjects[subj]] = [statistics, summary]
"""	
with open(directory + 'mycsvfile.csv','w', newline='') as f:
    w = csv.writer(f)
    for s in subjects:
	    w.writerow([s])
	    w.writerow([all_subj_data[s][0]])
	    for i in range(4):
		    w.writerow(all_subj_data[s][1][i])
"""	


#%% Display
plt.figure(1)
plt.subplot(1,2,1)
plt.plot(rr_sticky[:-1]*1/SR, delT_sticky*1000/SR); plt.title('RR-interval Sticky Electrode')
plt.xlabel('Time (s)'); plt.ylabel('RR-interval (ms)')
plt.subplot(1,2,2)
plt.plot(rr_dry[:-1]*1/SR, delT_dry*1000/SR); plt.title('RR-interval Dry Electrode')
plt.xlabel('Time (s)'); plt.ylabel('RR-interval (ms)')

"""
plt.figure(2)
plt.scatter(delT_sticky, delT_dry); plt.title('Linear Regression Sticky vs Dry')
plt.xlabel('Sticky Electrode'); plt.ylabel('Dry Electrodes')
z = np.polyfit(delT_sticky, delT_sticky, 1)
p = np.poly1d(z)
plt.plot(delT_sticky, p(delT_sticky), 'r-.')
"""

t_sticky = np.linspace(0,len(filtered_sticky)*1/SR, len(filtered_sticky))
t_dry = np.linspace(0,len(filtered_dry)*1/SR, len(filtered_dry))

plt.figure(3)
plt.subplot(2,1,1)
plt.plot(t_sticky, filtered_sticky); plt.title('Peak Detection in Sticky Electrodes')
for i in range(len(rr_sticky)):
	plt.axvline(x=(rr_sticky[i]-2)*1000/SR, color='r', linestyle='--')
plt.xlim(0,5000); plt.ylim(-200,400)
plt.xlabel('Time (ms)'); plt.ylabel('Voltage (mV)')

plt.subplot(2,1,2)
plt.plot(t_dry, filtered_dry); plt.title('Peak Detection in Dry Electrodes')
for i in range(len(rr_dry)):
	plt.axvline(x=(rr_dry[i]-2)*1000/SR, color='r', linestyle='--')
plt.xlim(0,5000); plt.ylim(-200,400)
plt.xlabel('Time (ms)'); plt.ylabel('Voltage (mV)')
plt.tight_layout()
	


# Animated figure

fig = plt.figure(4)
fig.set_size_inches(10,8)
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

ax1.plot(t_sticky,filtered_sticky); ax1.set_title('Peak Detection in Sticky Electrodes')
ax1.set_ylabel('Voltage (mV)'); ax1.set_xlabel('Time (s)')
for i in range(len(rr_sticky)):
	ax1.axvline(x=(rr_sticky[i]-3)*1/SR, color='r', linestyle='--')

ax2.plot(t_dry,filtered_dry); ax2.set_title('Peak Detection in Dry Electrodes')
ax2.set_ylabel('Voltage (mV)'); ax2.set_xlabel('Time (s)')
for i in range(len(rr_dry)):
	ax2.axvline(x=(rr_dry[i]-3)*1/SR, color='r', linestyle='--')

plt.tight_layout()

def animate(k):
	global filtered_sticky, filtered_dry
	
	
	ax1.set_xlim(0+.100*k,5+.1*k); ax1.set_ylim(-200,400)
	#ax1.set_xticklabels(range(0,len(filtered_dry),500))
	
	ax2.set_xlim(0+.100*k,5+.1*k); ax2.set_ylim(-200,400)
	#ax2.set_xticklabels(range(0,len(filtered_sticky),500))

ani = animation.FuncAnimation(fig, animate, frames=500, interval=1/SR) 
plt.show()

		
plt.rcParams['animation.ffmpeg_path'] ='C:\\ffmpeg-20200422-2e38c63-win64-static\\bin\\ffmpeg.exe'
ani.save('peakDetection.mp4', fps=10)



# 

