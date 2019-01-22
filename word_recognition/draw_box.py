import cv2
import numpy as np
import matplotlib.pyplot as plt
import pdb

path = 'final_words/'
img = cv2.imread('test.jpg')

words = []
with open('word_output.txt', 'r') as f:
	for line in f:
		line = line.strip()
		words.append(line)

positions = []
with open('positions.txt', 'r') as f:
	for line in f:
		line = line.strip().split(',')
		positions.append(line)

for i in range(len(positions)):
	pt1_x, pt1_y, pt2_x, pt2_y = list(map(int, positions[i]))
	word = words[i]
	roi = (img[pt1_y: pt2_y, pt1_x:pt2_x]!=(255, 255, 255)).nonzero()
	# plt.imshow(img[pt1_y: pt2_y, pt1_x:pt2_x, :])
	# plt.show()
	# pdb.set_trace()
	y1, x1 = min(roi[0]) + pt1_y, min(roi[1]) + pt1_x
	y2, x2 = max(roi[0])+ pt1_y, max(roi[1]) + pt1_x
	cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
	font = cv2.FONT_HERSHEY_TRIPLEX
	cv2.putText(img,word,(x1, y1), font, 1, (0,255,0), 2, cv2.LINE_AA)
	
cv2.imwrite('test_out.jpg', img)

