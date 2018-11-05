#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import sys
import os

list = 'canid.txt'
if(os.path.isfile(list) == False):
		sys.exit("Error")
with open(list, mode='r') as f:
	for line in f:
		line = line.replace('\r','')
		line = line.replace('\n','')
		line = line.replace('\r\n','')

		path_r = 'log/log_NT1000_{}.csv'.format(line)
		path_data_w = 'data/log_NT1000_{}_data.csv'.format(line)
		path_time_w = 'time/{}_Time.csv'.format(line)

		df = pd.read_csv(path_r, names=('Time','ID','P1','P2','P3','P4','P5','P6','P7','P8','D1','D2','D3','D4','D5','D6','D7','D8'))

		time = df['Time'][0:1000]
		time.to_csv(path_time_w,index=False)
		data = df[['P1','P2','P3','P4','P5','P6','P7','P8']][0:1000]
		data.to_csv(path_data_w,index=False)