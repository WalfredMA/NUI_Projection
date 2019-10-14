#!/usr/bin/python

import pandas as pd
import numpy as np
import scipy.misc
import math
import collections as cl
from scipy.optimize import curve_fit
import walfred_stats_tool as wal

#the instance used for downsampling 

class NUI_projection:
	
	#initiate current sample size, and target down sample sizes
	def __init__(self,current_size):

		self.current_size=current_size
		
	
	#used to find observed numbers of SVs respect to sample count for the SV. 
	def count(self,sample_counts):
		
		counts_data=cl.defaultdict(int)
		
		for x in sample_counts:
			counts_data[x]+=1
			
		#count data is storaged here, which is series V at current sample_size, the observed SV numbers at certain count.
		self.obs={count:obs for count, obs in counts_data.items() if count>1}
		
		return self
		
	
	#used to down sampling based on sample count of SVs 
	def downsample(self):
		
		#This is series of A as described in reasoning, A(sample_size,count)=V(sample_size,count)/combination(sample_size,count)
		#here we use log value to make sure it will not break the maximum integet size, to enhance the accuracy (python2 can only extend to 17 digits, but we are not sure if this is enough for log values), we used my own components to extend precisions.
		self.last_Aseries={k:pow(-wal.combination_log(self.current_size,k)+np.log2(np.longdouble(obs)),2) for k,obs in self.obs.items()}

		df_proj=[[self.obs[count] for count in sorted(self.obs.keys())]]
		
		for down_num in xrange(1, self.current_size-1):
			
			sample_size=self.current_size-down_num
			
			#series A follows binomial rule as described in reasoning. A(sample_size,count)= A(sample_size+1,count)+A(sample_size+1,count+1),
			#we use last A(sample_size+1) series to find current A(sample_size) series
			self.current_Aseries={count: self.last_Aseries[count] +  self.last_Aseries[count+1]  for count in xrange(2,sample_size+1)}
			self.last_Aseries=self.current_Aseries
			
			#find series V at down sample size based on series A
			row=[scipy.misc.comb(sample_size,count)*Aseries for count,Aseries in self.current_Aseries.items()]
			
			df_proj.append(row)
			
		#make it to be a dataframe
		self.downsample= pd.DataFrame.from_records(df_proj).T
		self.downsample.columns= range(2,self.current_size+1)[::-1]
		
		
		#sum up to find all expect NUIs at each sample size 
		self.SVcounts=map(sum,df_proj)[::-1]
	
		
		return self
	
	def upsample(self,targetsize,inits=[1000.0,0.00,10.00]):
		
		#the mathematical model used to predict NUI dicovery number at giving smaple size
		def incre_vs_samplesize(x, alpha, beta,gamma):
			
			return abs(alpha)/(x-1)+(10**beta)*(x-1)+abs(gamma)
		
		
		#find increment
		self.SVincre=[self.SVcounts[0]]+[x-y for x,y in zip(self.SVcounts[1:], self.SVcounts)]
		
		obs_sample_sizes=range(2,self.current_size+1)		
		
		#load x and y values
		xdata=obs_sample_sizes[-10:]
		ydata=self.SVincre[-10:]
		
		#fitting to find parameters
		para_fits = curve_fit(incre_vs_samplesize, xdata=xdata, ydata=ydata, p0=inits,method='lm')[0]
		
		self.para_fits=para_fits
		
		print 'fitted model: %f/x+%f*x+%f'%(abs(para_fits[0]), 2**para_fits[1], abs(para_fits[2]))
		
		#redefine model 
		def incre_vs_samplesize(x, alpha=abs(para_fits[0]), beta=2**para_fits[1],gamma=abs(para_fits[2])):
			
			return alpha/(x-1)+beta*(x-1)+gamma
		
		
		#projection based on model
		incres_proj=map(incre_vs_samplesize,range(self.current_size+1,targetsize+1))
		
		allincres=self.SVincre+incres_proj
		
		self.allSV_proj={}
		
		start=0
		for i,incre in enumerate(allincres):
			
			start+=incre
			self.allSV_proj[2+i]=start
		
		
		return self

#Packaging for the instance
def projection(allcounts, current_size,project_size):
	
	projection=NUI_projection(current_size).count(allcounts).downsample().upsample(project_size).allSV_proj
	
	return projection

	









