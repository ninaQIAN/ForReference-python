import re
import os
import json
import numpy as np
import scipy
from scipy import integrate
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

# butterworth
def butter_pass_filter(data, cutoff, fs, order):
	nyq = 0.5 * fs
	normal_cutoff = cutoff/nyq
	b, a = butter(order, normal_cutoff, btype='high', analog=False)
	y = lfilter(b, a, data)
	return y

def plotFilter(t, before, after):
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
	
	plt.grid()
	plt.legend()
	plt.show()
	


def Average(list):
	r=0.0
	for i in list:
		r+=i
	result=r/len(list)
	print round(result,3)

rootpath = "E:/study/2014Fall/special problem/data/run/"
#rootpath = "E:/study/2014Fall/special problem/data/test-walk/object1-han/"
filename_year = ""
filename_month = "20150117221922"
filename_date = ""


# find all files under target rootpath
list = os.listdir(rootpath)
#print list
prefix = filename_year+filename_month+filename_date
x = []
y = []
z = []
timestamp = []



for item in list:
	matchObj = re.match(prefix+'(.*)' , item, re.I)
	
	if matchObj:
		# find .log file of each given date 
		filename = matchObj.group()
		file = open(rootpath+filename,'r')

		for line in file.readlines():
			jsonData = json.loads(line)
			# prepared data	
			y.extend(jsonData['yAxis'])
			z.extend(jsonData['zAxis'])
			x.extend(jsonData['xAxis'])
			timestamp.extend(jsonData['sensorTimeStamps'])



# store x,y,z raw data
raw_data = []
raw_data.append(x)
raw_data.append(y)
raw_data.append(z)
totalcount = len(timestamp)

# Filter Requirements.
order = 2
cutoff = 0.25  # desired cutoff frequency of the filter, Hz
fs = totalcount/60       # sample rate, Hz
after_pass = butter_pass_filter(raw_data, cutoff, fs, order)

plotFilter(timestamp, raw_data,after_pass)

xtemp = np.array(after_pass[0])
ytemp = np.array(after_pass[1])
ztemp = np.array(after_pass[2])
width = 50
tt1 = 0

IA = []
print totalcount
for t1 in xrange(0, totalcount-1, width):
	
	a = []
	b = []
	xx = []
	yy = []
	zz = []
	
	if totalcount-t1-1 >= width:
		distance = width
		for j in xrange(t1, t1+distance-1,1):
			a.append(timestamp[j])
			xx.append(xtemp[j]*xtemp[j])
			yy.append(ytemp[j]*ytemp[j])
			zz.append(ztemp[j]*ztemp[j])
		xIA = np.trapz(xx,a)
		yIA = np.trapz(yy,a)
		zIA = np.trapz(zz,a)
		IA.append(xIA+yIA+zIA)

Average(IA)
