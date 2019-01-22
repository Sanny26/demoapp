import os
import cv2
import numpy as np
import pdb

files = os.listdir('words/')

for file in files:
	img = cv2.imread('words/'+file)
	w, h, _ = img.shape
	a1 = 255*np.ones((w, 50, 3))
	a2 = 255*np.ones((w, 50, 3))
	print(img.shape, a1[:, :, 0].shape)
	#pdb.set_trace()
	new_img = np.hstack([a1, img, a2])
	new_img = cv2.resize(new_img, (new_img.shape[1], 137))
	cv2.imwrite('n1words/'+file, new_img)


