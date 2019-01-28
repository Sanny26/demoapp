import cv2
import pdb
import matplotlib.pyplot as plt
import numpy as np
import os

repo = "seg_data/words/5"
pos_file = "seg_data/positions5.txt"
img = cv2.imread("hindi_pages/5.jpg")
pos = {}
with open(pos_file) as f:
	for line in f:
		line = line.strip().split(',')
		path = line[0]+line[1]
		# print(line, path)
		pos[path] = [int(line[i]) for i in range(2,6)]


for key, val in pos.items():
	#print(key)
	key = key.split('/')[2]
	cv2.rectangle(img, (val[2], val[0]), (val[3], val[1]), (255, 0, 0), 1)
	font = cv2.FONT_HERSHEY_COMPLEX_SMALL
	cv2.putText(img, key, (val[2], val[0]), font, 0.5, (255,0,0), 1, cv2.LINE_AA)

cv2.imwrite('out5.jpg', img)


