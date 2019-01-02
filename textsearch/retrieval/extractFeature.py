import torch
from torch.autograd import Variable
import torchvision.transforms as transforms

from skimage.color import rgb2gray
import numpy as np
import os
import cv2
import pdb
import time

from .model import * 
from .synthTransformer import Normalize, ToTensor

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

def preprocess(image, fontsize, transform=None):

    h,w = image.shape

    newWidth = np.min((int(np.ceil(((w*1.0)/h) * fontsize)),384-1))
    image = cv2.resize(image,(newWidth,fontsize))
    newImage = np.ones((128,384),dtype=np.float32) * 255.0

    rX = np.random.randint(0,384-newWidth)
    rY = np.random.randint(0,128-64)

    newImage[rY:fontsize+rY, rX:newWidth+rX] = image
    cords = np.where(newImage!=255)
    if cords[0].size==0:
        roi = np.asarray([0.0, 0.0,0.0, 100.0, 100.0],dtype=np.float32)
    else:
        roi = np.asarray([0.0, min(cords[1]),min(cords[0]),max(cords[1]),max(cords[0])],dtype=np.float32)

    sample = {'image': newImage, 'gt': 0, 'label': np.array(0), 'roi': roi}

    if transform:
        sample = transform(sample)

    return sample['image'].unsqueeze(0), sample['roi'].unsqueeze(0)


def feature(image, model_path):

    fontsize = 48
    transform_test = transforms.Compose([
    Normalize(),
    ToTensor()
    ])

    begin = time.time()
    image, roi = preprocess(image, fontsize, transform_test) 
    roi[:,0] = torch.arange(0,roi.size()[0])

    use_cuda = torch.cuda.is_available()
    if use_cuda:
        image, roi = image.cuda(), roi.cuda()
    
    image = image.unsqueeze(1)
    ptime = time.time() - begin

    with torch.no_grad():
        roi = Variable(roi)
        inputs = Variable(image)

        ## Loading model
        net = ResNetROI34(num_classes=8135)
        #print('==> Resuming from checkpoint..')
        checkpoint = torch.load(model_path, map_location='cpu')
        net.load_state_dict(checkpoint)
        net.eval()
        begin = time.time()
        outputs, outFeats = net(inputs, roi)
        featData = outFeats.cpu().data.numpy()
        print('Feature extract time', time.time()-begin)
    #L2 Normalize of features
    #normVal = np.sqrt(np.sum(featData**2,axis=1))
    #featData = featData/normVal[0]

    return featData


if __name__ == "__main__":
   img_path = "/Neutron6/santhoshini/small_set/uploads-2009-07-mohanlalblog6_01/2.jpg"
   img = cv2.imread(img_path)
   f = feature(img, "/Neutron6/santhoshini/models/new-iam.t7")
   pdb.set_trace()
