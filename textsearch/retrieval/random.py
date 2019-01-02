import cv2
import matplotlib.pyplot as plt 
import pickle

results = ['uploads-2016-03-page_7/6.jpg', 'uploads-2016-02-02/103.jpg', 'uploads-2015-12-page5/99.jpg', 'uploads-2013-09-page4/38.jpg', 'uploads-2016-09-page2/60.jpg', 'uploads-2013-06-Page3/40.jpg', 'uploads-2016-03-page_7/91.jpg',
 'uploads-2016-03-page_7/49.jpg', 'uploads-2013-09-page4/10.jpg', 'uploads-2017-08-page4/15.jpg']

wrd_pos_fpath = 'saved_models/positions.pkl'
with open(wrd_pos_fpath, 'rb') as fobj:
		wrd_pos = pickle.load(fobj)

each = results[0]
each = 'uploads-2016-03-page_7/7.jpg'
pos = [int(pos) for pos in wrd_pos[each]]
nimg_path = "media/cleaned/"+each.split('/')[0]+'.jpg'
nimg = cv2.imread(nimg_path)
nimg = cv2.rectangle(nimg, (pos[2], pos[0]), (pos[3], pos[1]), (0, 255, 0))
cv2.imwrite('test.jpg', nimg)