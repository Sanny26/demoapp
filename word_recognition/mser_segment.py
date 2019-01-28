import cv2
import pdb
import matplotlib.pyplot as plt
import numpy as np
import os

def refine(component):
    """Filter out extremely small components."""
    # plt.imshow(component, cmap='gray')
    # plt.show()
    area = component.shape[0]*component.shape[1]
    if area > 1000:
        return True
    return False

def extract_strokes(activated, img, out_folder):
    """Return the connectedComponents of the image."""
    nimg = cv2.connectedComponents(1-activated)[1]
    # Get the connectedComponents
    labels = set(np.unique(nimg))
    labels.remove(0)
    components = list()
    positions = list()
    line_information = list()

    counter = 0

    for label in labels:
        sub_region = (nimg == label).nonzero()
        max_hor = sub_region[1].max()
        min_hor = sub_region[1].min()
        max_ver = sub_region[0].max()
        min_ver = sub_region[0].min()
        word_img = img[min_ver:max_ver, min_hor:max_hor]
        counter+=1
        if refine(255-word_img):
            #components.append(word_img)
            #if counter==7:
            #    img[min_ver:max_ver, min_hor:max_hor] = 0
            #    plt.imshow(img, cmap='gray')
            #    plt.show()
            #    pdb.set_trace()
            pos = [min_ver//3, max_ver//3, min_hor//3, max_hor//3]
            pos = [str(int(each)) for each in pos]
            img_name = out_folder+str(counter)+'.jpg'
            ## each word image size will 1.5 times of its original size in the documents
            cv2.imwrite(img_name, word_img)
            out_writer.write(out_folder+', '+str(counter)+', '+ ", ".join(pos)+'\n')
            ann_writer.write(img_name + ', 0, 0, 0\n')

def get_file_name(file):
    path = file.split('-')

    return "{}/{}/{}/{}".format(path[0], path[1],path[2], "-".join(path[3:]))

def segment(img_folder, file):
    img = cv2.imread(img_folder+file)
    mser = cv2.MSER_create()
    file_name = img_folder+file
    grayscale_image = cv2.imread(file_name, 0)
    print(file_name)
    # pdb.set_trace()
    # Resize the image so that MSER can work better
    shape = (int(img.shape[1]*3), int(img.shape[0]*3)) 
    img = cv2.resize(img, shape)
    #pdb.set_trace()
    grayscale_image = cv2.resize(grayscale_image, shape)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    vis = img.copy()
    regions = mser.detectRegions(gray)
    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions[0]]


    points = []
    for i, each in enumerate(hulls):
        col_end, row_end = np.max(each[:, 0], axis = 0)
        col_start, row_start = np.min(each[:, 0], axis = 0)
        points.append([row_start, row_end, col_start, col_end])
        vis[row_start:row_end, col_start:col_end] = (0, 0, 0)

    kernel = np.ones((3, 20))
    dilated = 255-cv2.dilate(255-vis, kernel)
    cv2.imwrite('seg_data/regions/'+file, dilated)
    # plt.imshow(dilated, cmap='gray')
    # plt.show()
    # pdb.set_trace()
    gray = cv2.cvtColor(dilated, cv2.COLOR_BGR2GRAY)
    binary_img = cv2.threshold(gray, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    folder_name = 'seg_data/words/'+file.split('.')[0]+'/'
    os.mkdir(folder_name)
    extract_strokes(binary_img, grayscale_image, folder_name)

    
    

# segment('cleaned/', 'uploads-2012-05-Page3.jpg')
# pdb.set_trace()


img_folder = "hindi_pages/"
files = os.listdir(img_folder)

word_pos = dict()

for file in ['1.jpg']:
    out_file = "seg_data/positions{}.txt".format(file.split('.')[0])
    ann_file = "seg_data/ann{}.txt".format(file.split('.')[0])

    out_writer = open(out_file, "w")
    ann_writer = open(ann_file, "w")

    segment(img_folder, file)
    
    ann_writer.close()
    out_writer.close()
