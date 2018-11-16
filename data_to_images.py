#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################
###CANデータをRGB値に変換して可視化するプログラム###
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

#canidリストから対象とするCAN IDを取得
list = 'canid.txt'
if(os.path.isfile(list) == False):
		sys.exit("Error")
		
#パラメータ設定
window_size = 64 #行数
initial_bias = 4 #putpixelの回数
img = Image.new('RGB', (window_size,window_size))

print("Is it training data or varification data?(training:0 varification:1) ")
while True:
	flag = input()
	if flag == '0':
		path_rr = 'data/log_NT1000_{}_data.csv'
		path_ww = 'images/color/data_set/{}_{}_images.png'
		break
	elif flag == '1':
		path_rr = 'data/log_NT1000_{}_test.csv'
		path_ww = 'images/color/test/{}_{}_images.png'
		break
	else:
		print("Please type 0 or 1")

with open(list, mode='r') as fl:
	for id in fl:
		id = id.replace('\r','') #CAN IDリストの改行を排除
		id = id.replace('\n','')
		id = id.replace('\r\n','')

		cnt = 0
		bias = 0
		images_num = 0
		path_r = path_rr.format(id) #ログファイルの取得
		print(id)
		
		with open(path_r, mode='r') as fd:
			next(fd) #headerをスキップ
			for line in fd:
				data = line.split(',')
				#print(cnt)
				#print('{},{},{},{},{},{},{},{}'.format(int(data[0]),int(data[1]),int(data[2]),int(data[3]),int(data[4]),int(data[5]),int(data[6]),int(data[7])))
				img.putpixel((0+bias,cnt),(int(data[0]),int(data[1]),0)) #画素データを格納
				img.putpixel((1+bias,cnt),(int(data[2]),int(data[3]),0))
				img.putpixel((2+bias,cnt),(int(data[4]),int(data[5]),0))
				img.putpixel((3+bias,cnt),(int(data[6]),int(data[7]),0))
				
				bias = bias + initial_bias
				if bias == window_size:
					cnt = cnt + 1
					bias = 0
				if cnt  == window_size:
					path_w = path_ww.format(id,images_num) #保存する画像の名前とパスを指定
					#print(path_w)
					img.save(path_w)
					img = Image.new('RGB', (window_size, window_size))
					print(images_num)
					images_num = images_num + 1
					cnt = 0
