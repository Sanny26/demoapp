import cv2
import numpy as np
import matplotlib.pyplot as plt
import pdb
from PIL import ImageFont, ImageDraw, Image

path = 'doc1_words/'
img = cv2.imread('hindi_doc_1/page1.jpg')
bi = cv2.imread('hindi_doc_1/page1.jpg', 0)
ret,bi = cv2.threshold(bi,127,255,cv2.THRESH_BINARY)

words = []
with open('word_output.txt', 'r') as f:
	for line in f:
		line = line.strip()
		words.append(line)

positions = []
with open('doc1_positions.txt', 'r') as f:
	for line in f:
		line = line.strip().split(',')
		positions.append(line)

fontpath = "SakalBharati.ttf" # <== 这里是宋体路径 
font = ImageFont.truetype(fontpath, 10)
	
for i in range(len(positions)):
	pt1_x, pt1_y, pt2_x, pt2_y = list(map(int, positions[i]))
	word = 'शब्द'
	# pdb.set_trace()
	roi = (bi[pt1_y: pt2_y, pt1_x:pt2_x]!=255).nonzero()
	
	try:
		y1, x1 = min(roi[0]) + pt1_y, min(roi[1]) + pt1_x
		y2, x2 = max(roi[0])+ pt1_y, max(roi[1]) + pt1_x
	except:
		y1, x1 = pt1_y, pt1_x
		y2, x2 = pt2_y, pt2_x
	cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 1)
	# font = cv2.FONT_HERSHEY_COMPLEX_SMALL
	# cv2.putText(img,word,(x1, y1), font, 0.5, (255,0,0), 1, cv2.LINE_AA)
	img_pil = Image.fromarray(img)
	draw = ImageDraw.Draw(img_pil)
	draw.text((x1-5, y1-15),  word, font = font, fill = (255, 0, 0))
	img = np.array(img_pil)

cv2.imwrite('test_out.jpg', img)

