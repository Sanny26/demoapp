import cv2
import numpy as np
import matplotlib.pyplot as plt
import pdb
from PIL import ImageFont, ImageDraw, Image


def annotate(number):
	path = 'bin_data/{}'.format(number)
	img = cv2.imread('hindi_pages/{}.jpg'.format(number))
	bi = cv2.imread('hindi_pages/{}.jpg'.format(number), 0)
	ret,bi = cv2.threshold(bi,127,255,cv2.THRESH_BINARY)

	words = []
	with open('output{}.txt'.format(number), encoding='utf-8') as f:
		for line in f:
			line = line.strip()
			words.append(line)

	'''
	positions = []
	with open('seg_data/positions1.txt', 'r') as f:
		for line in f:
			line = line.strip().split(',')
			positions.append(line[2:])
	'''
	pos = {}
	with open('seg_data/positions{}.txt'.format(number)) as f:
		for line in f:
			line = line.strip().split(',')
			path = line[0]+line[1].strip()
			# print(line, path)
			pos[path] = [int(line[i]) for i in range(2,6)]

	fontpath = "font.ttf" 
	font = ImageFont.truetype(fontpath, 40)

	with open('seg_data/ann{}.txt'.format(number), 'r') as f:
		for i, line in enumerate(f):
			line = line.strip().replace('bin_data', 'seg_data').split('.')[0]
			# pdb.set_trace()

			pt1_y, pt2_y, pt1_x, pt2_x= list(map(int, pos[line]))
			# word = 'यदि'
			print(i)
			word = words[i]
			# pdb.set_trace()
			roi = (bi[pt1_y: pt2_y, pt1_x:pt2_x]!=255).nonzero()
			
			try:
				y1, x1 = min(roi[0]) + pt1_y, min(roi[1]) + pt1_x
				y2, x2 = max(roi[0])+ pt1_y, max(roi[1]) + pt1_x
			except:
				y1, x1 = pt1_y, pt1_x
				y2, x2 = pt2_y, pt2_x
			cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
			#ont = cv2.FONT_HERSHEY_COMPLEX_SMALL
			#cv2.putText(img,word,(x1, y1), font, 0.5, (255,0,0), 1, cv2.LINE_AA)
			img_pil = Image.fromarray(img)
			draw = ImageDraw.Draw(img_pil)
			draw.text((x1-15, y1-30),  word, font = font, fill = (0, 255, 0))
			img = np.array(img_pil)

	cv2.imwrite('final_out{}.jpg'.format(number), img)


#annotate(1)
#annotate(2)
#annotate(3)
#annotate(4)
#annotate(5)
annotate(6)
annotate(7)

