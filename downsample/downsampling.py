#!/usr/bin/python

import pandas as pd
import numpy as np
import scipy.misc
import math
import walfred_stats_tool as wal
	

#the instance used for downsampling 

class projection_downsample:
	
	#initiate current sample size, and target down sample sizes
	def __init__(self,current_size,target_samplesizes=[]):

		self.current_size=current_size
		
		self.target_samplesize=target_samplesizes
		
		if not len(self.target_samplesize):
			
			self.target_samplesize=range(2, self.current_size+1)
	
	#used to find observed numbers of SVs respect to sample count for the SV. 
	def count(self,sample_counts):
		
		counts_data=cl.defaultdict(int)
		
		for x in sample_counts:
			counts_data[x]+=1
			
		#count data is storaged here, which is series V at current sample_size, the observed SV numbers at certain count.
		self.obs={count:obs for count, obs in counts_data.items() if count>1}
		
		return self
		
	
	#used to down sampling based on sample count of SVs 
	def proj(self):
		
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
		
		
		return self
	
	#output to csv
	def output(self,outfile):
		
		
		self.downsample.to_csv(outfile,mode='w',index=False,sep=',')
		
		
		return self
	
	










