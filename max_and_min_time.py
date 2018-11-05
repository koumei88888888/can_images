#!/usr/bin/env python
# -*- coding: utf-8 -*-
#任意のファイルの各行の末尾に指定した文字を追加するプログラム(現在log_NT1000専用)
import sys
import os
import csv

args = sys.argv
if __name__ == '__main__':
	cnt = 0
	filename = args[1]
	if(os.path.isfile(filename) == False):
		sys.exit("Error")
	output = filename.replace(".csv","_label.csv")
	fo = open(output,mode='w',newline="")
	with open(filename,mode='r',newline="") as f:
		fo.write("Time,ID,P1,P2,P3,P4,P5,P6,P7,P8,D1,D2,D3,D4,D5,D6,D7,D8,Label,LabelText\n")
		for line in f:
			line = line.replace('\r','')
			line = line.replace('\n','')
			line = line.replace('\r\n','')
			
			if cnt > 1000:
				text = line+",1,abnormal\n"
				fo.write(text)
				#text = line+",0,normal\n" #normal:0 abnormal:1
			#else:
				#text = line+",1,abnormal\n"
			cnt = cnt + 1
			#fo.write(text)
	fo.close()