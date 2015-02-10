
import re
import os
import time
import json
import numpy as np
import scipy
from scipy import integrate
from scipy.signal import butter, lfilter, freqz, medfilt
import matplotlib.pyplot as plt
from numpy.fft import fft, fftn, fftfreq

	# xAxis: data[0]
	# yAxis: data[1]
	# zAxis: data[2]
	# timestamp: data[3]


def plot1(data,time):
	plt.figure(1)
	plt.plot(time,data[0],'r', label = "x")
	plt.plot(time,data[1],'b', label = "y")
	plt.plot(time,data[2],'g',label="z")
	plt.xlabel('time')
	plt.ylabel('walk')
	plt.grid()
	plt.legend()
	plt.show()


def plotFFT(freq,fftResult):
	plt.figure(5)
	plt.plot(50*freq, fftResult,'b-')
	plt.axis([0,10,0,700])
	plt.xlabel('freq')
	plt.ylabel('fftResult')
	plt.show()


def butter_pass_filter(data, cutoff, fs, order):
	nyq = 0.5 * fs # nyquist frequency
	normal_cutoff = cutoff/nyq
	b, a = butter(order, normal_cutoff, btype='high', analog=False)
	y = lfilter(b, a, data)
	return y

def butter_bandpass_filter(data, lowcut, highcut, fs, order):
	nyq = 0.5 * fs # nyquist frequency
	low = lowcut/nyq
	high = highcut/nyq
	b, a = butter(order, [low, high], btype='bandpass', analog=False)
	y = lfilter(b, a, data)
	return y


def SVMfunc(data):
	a = np.array(data[0])
	b = np.array(data[1])
	c = np.array(data[2])
	result = np.sqrt(a*a+b*b+c*c)
	return result



def readDataFromFile(rootpath, prefix):
	# find all files under target rootpath
	list = os.listdir(rootpath)
	#print list
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
	# Filter Requirements.
	order = 2
	fs = totalcount/(60*filenumber)       # sample rate, Hz
	cutoff = 0.25  # desired cutoff frequency of the filter, Hz
	# After Filter
	after_pass = butter_pass_filter(raw_data, cutoff, fs, order)
	#time domain SVM 
	SVM = SVMfunc(raw_data)
	plot1(after_pass,timestamp)




rootpath1 = "E:/study/2014Fall/special problem/data/run/"
rootpath2 = "E:/study/2014Fall/special problem/data/test-static/object1-han/"
rootpath3 = "E:/study/2014Fall/special problem/data/test-walk/object2-qian/"
filename1 = "20150117230737"
filename2 = "20150104180555"
filename3 = "20150105172133"

readDataFromFile(rootpath3,filename3)








walk = 4220 #1






#IA, err = integrate.quad(square_result, t1, t1+width)
#Energy_Expenditure = alpha * IA


