#!/usr/bin/python

import numpy as np


class precis:
	def __init__(self):
		
		self.num_seg=0
		self.int=0
		self.sign=0
		self.dec=[]
	
	def __str__(self):
			
		compliment=['', '0', '00', '000', '0000', '00000', '000000', '0000000', '00000000', '000000000', '0000000000', '00000000000', '000000000000', '0000000000000', '00000000000000', '000000000000000', '0000000000000000', '00000000000000000']
		
		print_str=''
		for x in self.dec:
			x_str=str(abs(x))
			if len(x_str)<10:
				x_str=compliment[10-len(x_str)]+x_str
			print_str+=x_str
		
		return str(self.int)+'.'+print_str
	
	def __repr__(self):
		return str(self)
		
	def resort(self):
		
		sums=[self.int]
		
		if self.int>0:
			sign=1
		elif self.int<0:
			sign=-1
		else:
			sign=0
			

		for x in self.dec:
			
			if x>10000000000:
	
				sums[-1]+=x/10000000000
				x%=10000000000
				
			elif x<-10000000000:
				
				sums[-1]-=x/-10000000000
				x%=-10000000000
			
			if x>0:
				current_sign=1
			elif x<0:
				current_sign=-1
			else:
				current_sign=0
			
			if current_sign*sign<0:
				
				sums[-1]+=-sign
				x=sign*10000000000+x
			
			if not sign:
				sign=current_sign
			
			sums.append(x)
		
		
		self.int=sums[0]
		
		self.dec=sums[1:]
		
		self.sign=sign
		
	
	
class precis_cal(precis):
	
	def __init__(self, x, num_seg=3):
		
		
		self.int=int(x)
		
		if x<0:
			self.sign=-1
		else:
			self.sign=1
		
		dec=x-self.int
		
		self.num_seg=num_seg
				
		thefactor=10**10
		
		allsegs=[]
		
		remainder=dec
		for i in xrange(num_seg):
			
			remainder*=thefactor
			quotient=int(remainder)
			remainder-=quotient
			allsegs.append(quotient)
			
		
		self.dec=allsegs
		
	
	
		
	def __add__(self,another):
		
		thesum=precis_cal(0,0)
		
		if isinstance(another, precis_cal):
			
			
			if self.num_seg>=another.num_seg:
				addpairs=map(sum,list(zip(self.dec,another.dec))+[(x,0) for x in self.dec[:(self.num_seg-another.num_seg)]])
			else:
				addpairs=map(sum,list(zip(self.dec,another.dec))+[(0,x) for x in another.dec[:(another.num_seg-self.num_seg)]])		
			
			thesum.num_seg=len(addpairs)
			
			thesum.int=another.int+ self.int
			
			thesum.dec=addpairs
			
			thesum.sign=self.sign
			
			thesum.resort()
			
			
		
		elif type(another)==type(0):
			
			
			thesum.int+=another
			
			thesum.num_seg=self.num_seg
			
			thesum.dec=self.dec
			
			thesum.sign=self.sign
		
		else:
			
			thesum=self+precis_cal(another)
			
		
		return thesum
	
	def __radd__(self, another):
		
		if isinstance(another, precis_cal):
			
			return self+another
	
	def __mul__(self, factor):
			
		if isinstance(factor, int):
			
			
			new=precis_cal(0,0)
			new.dec=[x*factor for x in self.dec]
			new.int=self.int*factor
			new.num_seg=self.num_seg
			new.resort()
			
			
		
		return new
		
				
				
	def __neg__(self):
		
		new=precis_cal(0,0)
		new.num_seg=self.num_seg
		new.int=-self.int
		new.sign=-self.sign
		new.dec=[-x for x in self.dec]
		
		return new
		
	def __sub__(self,another):
		
		return self+ -another
		

	def __pow__(self, base):
		
		if not len(self.dec):
			return base**self.int
			
		start=base**(float(self.dec[0])/10**10+self.int)
		
			
		for i,x in enumerate(self.dec[1:]):
			
			start*=base**(float(x)/10**(10*(i+2)))
		
		return start


def combination_log(total,obs):
	
	def sum(sequence):
		
		if not len(sequence):
			return 0
			
		start=sequence[0]
		for value in sequence[1:]:
			start = start + value
		return start
	
	result=[precis_cal(np.log2(np.longdouble(x))) for x in xrange(total-obs+1, total+1)]+[precis_cal(-np.log2(np.longdouble(x))) for x in xrange(2, obs+1)]
	
	
	return sum(result)
	

