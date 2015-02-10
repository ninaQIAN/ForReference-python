import re
import os
import time
import json
import numpy as np
import scipy
from scipy import integrate
from scipy.signal import butter, lfilter, freqz, medfilt
from numpy.fft import fft, fftn, fftfreq
import matplotlib.pyplot as plt


	# xAxis: data[0]
	# yAxis: data[1]
	# zAxis: data[2]
	# timestamp: data[3]

def plot1(data,time):
	plt.figure(1) 
	plt.subplot(4,1,1)
	plt.plot(time,data[0])
	plt.xlabel('timestamp')
	plt.ylabel('xAxis')
	
	plt.subplot(4,1,2)
	plt.plot(time,data[1])
	plt.xlabel('timestamp')
	plt.ylabel('yAxis')
	
	plt.subplot(4,1,3)
	plt.plot(time,data[2])
	plt.xlabel('timestamp')
	plt.ylabel('zAxis')
	
	plt.subplot(4,1,4)
	plt.plot(time,data[3])
	plt.xlabel('timestamp')
	plt.ylabel('SVM')
	
	plt.show()
	
	
	
def plot2(data,time):
	plt.figure(2)
	plt.plot(time,data[0],'r', time,data[1],'b', time,data[2],'g', time,data[3],'pink')
	plt.xlabel('timestamp')
	plt.ylabel('data')
	plt.show()
	
	
	
def plotFilter(t, before, after):
	plt.figure(4) 
	plt.subplot(3,1,1)
	plt.plot(t,before[0],'b-',label='before')
	plt.plot(t, after[0], 'g-', linewidth=2, label='after')
	plt.xlabel('sensorTimeStamps [millisec]')
	plt.ylabel('xAxis')
	plt.grid()
	
	plt.subplot(3,1,2)
	plt.plot(t,before[1],'b-',label='before')
	plt.plot(t, after[1], 'g-', linewidth=2, label='after')
	plt.xlabel('sensorTimeStamps [millisec]')
	plt.ylabel('yAxis')
	plt.grid()
	
	plt.subplot(3,1,3)
	plt.plot(t,before[2],'b-',label='before')
	plt.plot(t, after[2], 'g-', linewidth=2, label='after')
	plt.xlabel('sensorTimeStamps [millisec]')
	plt.ylabel('zAxis')	
	plt.grid()
	plt.legend()
	plt.show()
	
def plotMed(t, before, after):
	plt.figure(4) 
	plt.subplot(3,1,1)
	plt.plot(t,before[0],'b-',label='before')
	plt.plot(t, after[0], 'g-', linewidth=2, label='after')
	plt.xlabel('sensorTimeStamps [millisec]')
	plt.ylabel('xAxis')
	
	plt.subplot(3,1,2)
	plt.plot(t,before[1],'b-',label='before')
	plt.plot(t, after[1], 'g-', linewidth=2, label='after')
	plt.xlabel('sensorTimeStamps [millisec]')
	plt.ylabel('yAxis')
	
	plt.subplot(3,1,3)
	plt.plot(t,before[2],'b-',label='before')
	plt.plot(t, after[2], 'g-', linewidth=2, label='after')
	plt.xlabel('sensorTimeStamps [millisec]')
	plt.ylabel('zAxis')
	plt.legend()
	plt.show()
	
def SVMfunc(data):
	a = np.array(data[0])
	b = np.array(data[1])
	c = np.array(data[2])
	result = np.sqrt(a*a+b*b+c*c)
	return result
	

def butter_bandpass_filter(data, lowcut, highcut, fs, order):
	nyq = 0.5 * fs # nyquist frequency
	low = lowcut/nyq
	high = highcut/nyq
	b, a = butter(order, [low, high], btype='bandpass', analog=False)
	y = lfilter(b, a, data)
	return y

def plotFreq(freq,fftResult):
	plt.figure(5)
	plt.plot(50*freq, fftResult,'b-')
	plt.axis([0,10,0,5000])
	plt.xlabel('freq')
	plt.ylabel('fftResult')
	plt.show()


rootpath = "E:/study/2014Fall/special problem/data/run/"
#rootpath = "E:/study/2014Fall/special problem/data/test-walk/object2-qian/"
filename_year = "20150121171"
filename_month = "4"
filename_date = ""


# find all files under target rootpath
list = os.listdir(rootpath)
#print list
prefix = filename_year+filename_month+filename_date
x = []
y = []
z = []
timestamp = []
filenumber = 0
filecount = []

for item in list:
	matchObj = re.match(prefix+'(.*)' , item, re.I)
	
	if matchObj:
		# find .log file of each given date 
		filename = matchObj.group()
		file = open(rootpath+filename,'r')
		filenumber = filenumber+1
		for line in file.readlines():
			jsonData = json.loads(line)
			# prepared data	
			y.extend(jsonData['yAxis'])
			z.extend(jsonData['zAxis'])
			x.extend(jsonData['xAxis'])
			timestamp.extend(jsonData['sensorTimeStamps'])
			# data amount of each sample
			temp = []
			temp.extend(jsonData['sensorTimeStamps'])
			filecount.append(len(temp))


# store x,y,z raw data
raw_data = []
raw_data.append(x)
raw_data.append(y)
raw_data.append(z)

# total timestamp
totalcount = len(timestamp)

# Median filter
#after_med = []
#after_med = medfilt(raw_data,3) # length if median = kernel_size
#plotMed(timestamp, raw_data,after_med)

# Filter Requirements.
order = 2
fs = totalcount/(60*filenumber)       # sample rate, Hz
lowcut = 0.5  # desired cutoff frequency of the filter, Hz
highcut = 5


# After Filter
after_pass = butter_bandpass_filter(raw_data, lowcut, highcut, fs, order)

# after_pass[0] x
# after_pass[1] y
# after_pass[2] z


# t, before, after
# plot both the original and filtered signals
#plotFilter(timestamp, raw_data,after_pass)


# after_pass[3] SVM

#time domain SVM 
svm = SVMfunc(raw_data)

# all axis
#plot1(after_pass,timestamp)
# only svm
#plot2(after_pass,timestamp)





out1 = fft(svm)
fftresult = np.abs(out1) 
n = svm.size
freq = fftfreq(n,d=1)

max_index = np.argmax(fftresult[1:])

print 50*np.abs(freq[max_index])

plotFreq(freq,fftresult)



