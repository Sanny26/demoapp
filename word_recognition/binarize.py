import cv2
import os
import matplotlib.pyplot as plt
import pdb

infolder = "seg_data/"
outfolder = "bin_data/"

os.mkdir(outfolder)

folders  = os.listdir(infolder)
for folder in folders:
	fpath = infolder + folder +'/'
	if len(fpath.split('.')) == 1:
		os.mkdir(outfolder + folder +'/')
		files = os.listdir(fpath)
		for file in files:
			if file.split('.')[1]=='jpg':
				filepath = fpath+file 
				img = cv2.imread(filepath,0)
				ret,thresh1 = cv2.threshold(img,150,255,cv2.THRESH_BINARY)
				cv2.imwrite(outfolder+folder +'/'+ file, thresh1)

