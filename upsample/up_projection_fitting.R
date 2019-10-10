library(minpack.lm)

#function to generate cumulative vector
cul<-function(list){	
	out<-c()
	thesum<-0
	for (x in list){
		
		thesum<-thesum+x
		out<-c(out,thesum)
	}	
	return (out)	
}


#up sampling function based on putative mathematic model

upproj<-function(data,upsample_num){
	
	#data: total SV number at all sample size based on downsampling 
	#upsample_num: up-sampling until
	
	
	len_d<-length(data)
	
	#generate increment dataset
	data_incre<-rev(data)[2:len_d]-rev(data)[1:(len_d-1)]
	ratio_df<-data.frame(sample_num=c(1:(len_d-1)),incre=data_incre)
	
	#initiate parameters for fitting
	starts<-list(limit=0.00001,ceof=2000)
	
	#fitting for the increments
	ratio_fit<-nlsLM(incre ~ (limit*sample_num+ceof/sample_num)  , data =  ratio_df[(len_d-11):(len_d-1),], start = starts,control = nls.control(1000))		

	#used fitting model for upsampling
	up_samplesize<-data.frame(sample_num=c((len_d):(upsample_num-1)))	
	upproj<-predict(ratio_fit,newdata=up_samplesize)
	
	#combine with old data 
	new_data_incre<-c(data_incre, upproj)
	
	#use increments to find expect data
	new_data<-cul(c(rev(data)[1],new_data_incre))
		
	return (new_data)

	
}