'''
Created on Mar 16, 2013

@author: tiago

Adapted to Bruce Randall's LockinAmp application
by Dave Cohen
'''

import numpy as np
from scipy.interpolate import UnivariateSpline
from scipy.signal import wiener, filtfilt, butter, gaussian, freqz
from scipy.ndimage import filters
import scipy.optimize as op
import matplotlib.pyplot as plt
import csv

def ssqe(sm, s, npts):
	return np.sqrt(np.sum(np.power(s-sm,2)))/npts

def testGauss(x, y, s, npts):
	#b = gaussian(39, 10)
	b = gaussian(75, 15)
	#ga = filtfilt(b/b.sum(), [1.0], y)
	ga = filters.convolve1d(y, b/b.sum())
	plt.plot(x, ga)
	print "gaerr", ssqe(ga, s, npts)
	return ga

def testButterworth(nyf, x, y, s, npts):
	b, a = butter(4, 1.5/nyf)
	fl = filtfilt(b, a, y)
	plt.plot(x,fl)
	print "flerr", ssqe(fl, s, npts)
	return fl

def testWiener(x, y, s, npts):
	wi = wiener(y, mysize=29, noise=0.5)
	plt.plot(x,wi)
	print "wieerr", ssqe(wi, s, npts)
	return wi

def testSpline(x, y, s, npts):
	sp = UnivariateSpline(x, y, s=240)
	plt.plot(x,sp(x))
	print "splerr", ssqe(sp(x), s, npts)
	return sp(x)

def plotPowerSpectrum(y, w):
	ft = np.fft.rfft(y)
	ps = np.real(ft*np.conj(ft))*np.square(dt)
	plt.plot(w, ps)

if __name__ == '__main__':

	# Number of lines in header
	HEADERSIZE = 5
	# Number of lines to skip in beginning of file (after header)
	dataStart = 700
	# Number of lines to skip at end of file
	skipEnd = 4000
	count = 0
		
	# Y is a list of the CSV data
	Y = []
	
	# Need the size of the CSV file (less headers)
	numLines = 0
	
	# Open the file
	inputfile = "20151024_CassA.csv"
	f = open(inputfile, 'rt')
	
	try:
		# Read the file as a CSV, comma-delimited and ' quoted
		reader = csv.reader(f)          # this id just to get the number of lines in the file
		count = sum(1 for _ in reader)  # counting lines now
		f.seek(0)                       # reset the file pointer
		reader = csv.reader(f)          # reset the csv reader to actually read data
		dataEnd = count - skipEnd       # the end of the data, or the last line
		
		# Skip the first 5 header lines of the file, and whatever number of start and end records desired
		#for line in range(dataStart):
		for line in range(HEADERSIZE + dataStart):
			next(reader)
			
		for row in reader:	
			Y.append(float(row[2]))
			print float(row[2])
			numLines += 1
			# This is ugly - I throw exception if program goes past end of data
			if numLines > dataEnd:
				raise Exception()
			
	except:
		pass # something needs to be here
			
	finally:
		# Close file when done
		f.close()
	
	s = np.array(Y)
	npts = numLines
	end = numLines
	dt = end/float(npts)
	nyf = 0.5/dt
	sigma = 0.5 
	x = np.arange(end)
	y = s
	
	# Plot the raw signal
	plt.xlim([0,end]) # set the xlimit so the data just fits in the graph
	plt.plot(x,y)
	
	# Plot the filtered signal
	ga = testGauss(x, y, s, npts)
	#fl = testButterworth(nyf, x, y, s, npts)
	#wi = testWiener(x, y, s, npts)
	#sp = testSpline(x, y, s, npts)
	#plt.legend(['true','meas','gauss','iir','wie','spl'], loc='upper center')
	plt.legend(['meas','gauss'], loc='upper center')
	plt.savefig("signalvsnoise.png")
	plt.show()
	plt.clf()