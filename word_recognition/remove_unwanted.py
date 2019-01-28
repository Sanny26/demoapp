import cv2
import pdb
import matplotlib.pyplot as plt
import numpy as np
import os


def remove(number):
	repo = "seg_data/{}".format(number)
	pos_file = "seg_data/positions{}.txt".format(number)
	ann_file = "seg_data/ann{}.txt".format(number)
	bin_file = "bin_data/{}/".format(number)
	pos = {}
	with open(ann_file, 'w') as f1:
		with open(pos_file, 'r') as f:
			for line in f:
				line = line.strip().split(',')
				path = line[0]+line[1].strip()+'.jpg'
				nath = bin_file+line[1].strip()+'.jpg'
				# print(path)
				if os.path.isfile(path):
					f1.write(nath+'\n')


remove(1)
remove(2)
remove(3)
remove(4) 
remove(5) 
remove(6)
remove(7)  