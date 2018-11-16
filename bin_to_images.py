#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################
###CANデータを2進数に変換して可視化するプログラム###
###製作者：上村孔明                              ###
###作成日：2018/11/05                            ###
###更新日：2018/11/05                            ###
###version1.0                                    ###
###説明：パラメータの行数を指定することで正方形  ###
###に可視化された画像を生成できる。CANデータ1つ分###
###を4画素に割り振っているのでbias分右にシフトして###
###パケットを連結することで正方形に形成している  ###
####################################################

import pandas as pd
import sys
import os
from PIL import Image

debug = 0

#canidリストから対象とするCAN IDを取得
list = 'canid.txt'
if(os.path.isfile(list) == False):
		sys.exit("Error")
		
#パラメータ設定
window_size = 64 #行数
initial_bias = 8 #CANのバイト数
img = Image.new('1', (window_size,window_size))

print("Is it training data or varification data?(training:0 varification:1) ")
while True:
	flag = input()
	if flag == '0':
		path_rr = 'data/log_NT1000_{}_data.csv'
		path_ww = 'images/BW/data_set/{}_{}_images.png'
		break
	elif flag == '1':
		path_rr = 'data/log_NT1000_{}_test.csv'
		path_ww = 'images/BW/test/{}_{}_images.png'
		break
	else:
		print("Please type 0 or 1")

with open(list, mode='r') as fl:
	for id in fl:
		id = id.replace('\r','') #CAN IDリストの改行を排除
		id = id.replace('\n','')
		id = id.replace('\r\n','')

		images_num = 0
		mask = 1
		y = 0
		path_r = path_rr.format(id) #ログファイルの取得
		print(id)
		
		with open(path_r, mode='r') as fd:
			next(fd) #headerをスキップ
			for line in fd:
				#if debug == 1:
				#	exit()
				line = line.replace('\r','')
				line = line.replace('\n','')
				line = line.replace('\r\n','')
				print(line)
				x = 0
				bias = initial_bias - 1
				data = line.split(',')
				#print('{},{},{},{},{},{},{},{}'.format(int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]),int(data[6]),int(data[7])))
				for i in range(initial_bias):
					#print("bias:%d"%bias)
					data[i] = int(data[i])
					#print("data[{}]:{}".format(i,data[i]))
					for _ in range(8):
						print(bin(data[i]))
						#print("mask:%d"%mask)
						if data[i] & mask == 0:
							img.putpixel((bias-x,y),1)
							#print("put white")
						else:
							img.putpixel((bias-x,y),0)
							#print("put black")
						data[i] = data[i] >> 1
						x = x + 1
					bias = bias + initial_bias * 2
				y = y + 1
				if y  == window_size:
					path_w = path_ww.format(id,images_num) #保存する画像の名前とパスを指定
					img.save(path_w)
					img = Image.new('1', (window_size, window_size))
					#print(images_num)
					images_num = images_num + 1
					y = 0
				#debug = debug + 1
