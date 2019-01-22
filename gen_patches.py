import os
import cv2
import random
import matplotlib.pyplot as plt

input_folder = 'imprint_demo/static/docs/resolution/IP/'
output_folder = 'imprint_demo/static/docs/resolution/res/'

input_files = os.listdir(input_folder)
patch_in_images = 'imprint_demo/static/docs/resolution/patch_input/images/'
patch_in_patches = 'imprint_demo/static/docs/resolution/patch_input/patches/'
patch_out_images = 'imprint_demo/static/docs/resolution/patch_output/images/'
patch_out_patches = 'imprint_demo/static/docs/resolution/patch_output/patches/'

for file in input_files:
	ifile = input_folder + file
	fid = file.split('.')[0]
	# ofile = output_folder + fid + '_output.png'
	ofile = output_folder + fid + '.png'
	img_1 = cv2.imread(ifile)
	img_2 = cv2.imread(ofile)
	print(ofile)
	h, w, _ = img_1.shape
	pw, ph = 400, 300
	print(w, pw, h, ph)
	os.makedirs(patch_in_images+fid)
	os.makedirs(patch_out_images+fid)
	os.makedirs(patch_in_patches+fid)
	os.makedirs(patch_out_patches+fid)
	for i in range(1, 15):
		x = random.randint(10, h-ph-5)
		y = random.randint(10, w-pw-5)
		pt1 = (x, y)
		pt2 = (x+ph, y+pw)
		
		img1 = img_1.copy()
		cv2.rectangle(img1, (y, x), ( y+pw, x+ph) , (0,255,0), 3)
		patch = img_1[pt1[0]:pt2[0], pt1[1]:pt2[1]]
		# plt.imshow(img)
		# plt.show()
		# plt.imshow(patch)
		# plt.show()
		cv2.imwrite('{}/{}.jpg'.format(patch_in_images+fid, i), img1)
		cv2.imwrite('{}/{}.jpg'.format(patch_in_patches+fid, i), patch)

		img2 = img_2.copy()
		cv2.rectangle(img2, (y, x), ( y+pw, x+ph) , (0,255,0), 3)
		patch = img_2[pt1[0]:pt2[0], pt1[1]:pt2[1]]
		# plt.imshow(img)
		# plt.show()
		# plt.imshow(patch)
		# plt.show()
		cv2.imwrite('{}/{}.jpg'.format(patch_out_images+fid, i), img2)
		cv2.imwrite('{}/{}.jpg'.format(patch_out_patches+fid, i), patch)


