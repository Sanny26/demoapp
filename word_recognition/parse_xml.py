import xml.etree.ElementTree as ET
import pdb
import cv2

tree = ET.parse('test.xml')
root = tree.getroot()
words = root.findall('object')
word_dir = 'words/'

img = cv2.imread('test.jpg')
with open('positions.txt', 'w') as f1:
	with open('demo_tann.txt' ,'w') as f:
		for i, obj in enumerate(words):
			polygon_pts = obj.findall('polygon')[0].findall('pt')
			pt1_x = polygon_pts[0].find('x').text
			pt1_y = polygon_pts[0].find('y').text
			pt2_x = polygon_pts[2].find('x').text
			pt2_y = polygon_pts[2].find('y').text
			word = img[int(pt1_y):int(pt2_y), int(pt1_x):int(pt2_x)]
			cv2.imwrite('{}{}.jpg'.format(word_dir, i), word)
			f1.write('{}, {}, {}, {}\n'.format(pt1_x, pt1_y, pt2_x, pt2_y))
			f.write('HindiSeg/words/'+str(i)+'.jpg\n')
# pdb.set_trace()
