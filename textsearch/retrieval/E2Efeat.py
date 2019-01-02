import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn

import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.optim.lr_scheduler import StepLR
from torch.autograd import Variable

from .deepmodels import *
from .E2EsynthTransformer import Normalize, ToTensor
from .phoc import *

import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

use_cuda = torch.cuda.is_available()

transform_test = transforms.Compose([
    Normalize(),
    ToTensor()
])


def l2Normalize(inputTensor):
    normVal = torch.norm(inputTensor, p=2, dim=1).unsqueeze(1)
    normTensor = inputTensor.div(normVal.expand_as(inputTensor))
    return normTensor

def synthesizeImage(rText):
    font_path = 'saved_models/Lohit-Malayalam.ttf'
    rText.encode('utf-8')
    rFontIdx = 0
    #fontsize = 48
    #font = ImageFont.truetype(font_path, fontsize)
    #w, h = font.getsize(rText)
    font = ImageFont.truetype(font_path, 32)
    w, h = font.getsize(rText)
    # elif(w<64):
    #     font = ImageFont.truetype(self.font_paths[rFontIdx], 96)
    #     w, h = font.getsize(rText)

    image = Image.new('L', (384,128), 'white')

    brush = ImageDraw.Draw(image)
    brush.text((0, 0), rText, font=font, fill=0)

    #Converting image to np array to support opencv operations
    image = np.array(image).astype(np.float32)
    cords = np.where(image!=255)

    roi = np.asarray([0.0, min(cords[1]),min(cords[0]),max(cords[1]),max(cords[0])],dtype=np.float32)

    sample = {'image': image, 'roi': roi}
    cv2.imwrite('synthimg.jpg', sample['image'])
    return sample

def phocVec(text):
    phoc_gr_file = '/home/sanny/wordspotting/saved_models/grams.npz'
    phoc_files = np.load(phoc_gr_file)
    phoc_unigrams = phoc_files['arr_0'].tolist()
    phoc_bigrams = phoc_files['arr_1'].tolist()

    phoc_mat = build_phoc([text], phoc_unigrams, [1,2,3,4,5,6,7,8,9,10], \
                        bigram_levels=[2,3,4,5,6], phoc_bigrams=phoc_bigrams,on_unknown_unigram='warn')
    return phoc_mat

def preprocess_text(text, fontsize, transform):
    image = np.ones((32,32),dtype=np.float32) * 255.0
    h,w = image.shape
    newWidth = np.min((int(np.ceil(((w*1.0)/h) * fontsize)),384-1))
    image = cv2.resize(image,(newWidth,fontsize))
    newImage = np.ones((128,384),dtype=np.float32) * 255.0
    rX = 0
    rY = 0
    newImage[rY:fontsize+rY, rX:newWidth+rX] = image
    cords = np.where(newImage!=255)
    if cords[0].size==0:
        roi = np.asarray([0.0, 0.0,0.0, 100.0, 100.0],dtype=np.float32)
    else:
        roi = np.asarray([0.0, min(cords[1]),min(cords[0]),max(cords[1]),max(cords[0])],dtype=np.float32)

    synth_sample = synthesizeImage(text)
    phoc_vec = phocVec(text)
    phoc_vec = torch.from_numpy(phoc_vec)

    sample = {'image': synth_sample['image'], 'roi': synth_sample['roi']}
    if transform:
        sample = transform(sample)

    return sample['image'].unsqueeze(0), sample['roi'].unsqueeze(0), phoc_vec, synth_sample['image']

def preprocess_img(image,fontsize, transform):
    h,w = image.shape
    newWidth = np.min((int(np.ceil(((w*1.0)/h) * fontsize)),384-1))
    image = cv2.resize(image,(newWidth,fontsize))
    newImage = np.ones((128,384),dtype=np.float32) * 255.0

    rX = 0
    rY = 0
    newImage[rY:fontsize+rY, rX:newWidth+rX] = image
    cords = np.where(newImage!=255)
    if cords[0].size==0:
        roi = np.asarray([0.0, 0.0,0.0, 100.0, 100.0],dtype=np.float32)
    else:
        roi = np.asarray([0.0, min(cords[1]),min(cords[0]),max(cords[1]),max(cords[0])],dtype=np.float32)

    sample = {'image': newImage, 'roi': roi}

    if transform:
        sample = transform(sample)

    return sample['image'].unsqueeze(0), sample['roi'].unsqueeze(0)


def txtFeat(text, pretrained_path, synthArch='spp', embedSize=2048, testAug=False):
    '''
    synthArch: roi/spp
    '''
    if testAug:
        testFontSizes = [48,32,64]
    else:
        testFontSizes = [48]
    for tSize in testFontSizes:
        checkpoint = torch.load(pretrained_path, map_location='cpu')

        if synthArch=='roi':
            synthNet = hwnetSynth(phocVecSize=6005)
        elif synthArch=='spp':
            synthNet = hwnetSynthSPP(spp_level=3, phocVecSize=6005)
    
        embedNet = csNet(numClasses=9269,embedSize=embedSize)  #Here 8134 refers to #classes in IAM. Not important for feature computation; Todo: Remove its dependency

        synthNet.load_state_dict(checkpoint['synthNet'])
        embedNet.load_state_dict(checkpoint['embedNet'])

        if use_cuda:
            synthNet.cuda()
            embedNet.cuda()
            
            synthNet = torch.nn.DataParallel(synthNet, device_ids=list(range(torch.cuda.device_count())))
            embedNet = torch.nn.DataParallel(embedNet, device_ids=list(range(torch.cuda.device_count())))
            cudnn.benchmark = True
    
        synthNet.eval()
        embedNet.eval()

        features = []
        for word in text:
            inputs_2, roi_2, phoc, synth_img = preprocess_text(word, tSize, transform_test)        
            
            with torch.set_grad_enabled(False):
                roi_2[:,0] = torch.arange(0,roi_2.size()[0])

                if use_cuda:
                    inputs_2, roi_2, phoc = inputs_2.cuda(), roi_2.cuda(), phoc.cuda()

                inputs_2 = inputs_2.unsqueeze(1)
                
                outSynthFeats = synthNet(inputs_2, roi_2, phoc)
                outSynthFeats = l2Normalize(outSynthFeats)
                outSynthClassScores, outSynthEmbed = embedNet(outSynthFeats)

                outSynthEmbed = l2Normalize(outSynthEmbed)
                featSynthData = outSynthEmbed.cpu().data.numpy()
                features.append(featSynthData[0,:])
    # to do: for test augmentation
    # if args.featType<=1:
    #     maxFeatMat = np.amax(featImgMat,axis=0)
    # if not(args.featType==1):
    #     maxSynthMat = np.amax(featSynthMat,axis=0)

    ## converting synthetic image tensor to numpy
    return np.array(features)


def imgFeat(img, pretrained_path, arch='resnetROI34SPP',embedSize=2048, testAug = False):
    '''
    arch= 'resnetROI34SPP'/ 'resnetROI34'
    '''
    if testAug:
        testFontSizes = [48,32,64]
    else:
        testFontSizes = [48]
    for tSize in testFontSizes:
        checkpoint = torch.load(pretrained_path, map_location='cpu')

        if arch=='resnetROI34':
            net = ResNetROI34()
        elif arch=='resnetROI34SPP':
            net = ResNetROI34SPP(spp_level=3)

        embedNet = csNet(numClasses=9269,embedSize=embedSize)  #Here 8134 refers to #classes in IAM. Not important for feature computation; Todo: Remove its dependency

        net.load_state_dict(checkpoint['net'])
        embedNet.load_state_dict(checkpoint['embedNet'])

        if use_cuda:
            net.cuda()
            net = torch.nn.DataParallel(net, device_ids=list(range(torch.cuda.device_count())))
            embedNet.cuda()
            embedNet = torch.nn.DataParallel(embedNet, device_ids=list(range(torch.cuda.device_count())))
            cudnn.benchmark = True
    
        net.eval()
        embedNet.eval()

        inputs_1, roi_1 = preprocess_img(img, tSize, transform_test)
        with torch.set_grad_enabled(False):
            roi_1[:,0] = torch.arange(0,roi_1.size()[0])
            if use_cuda:
                inputs_1, roi_1 = inputs_1.cuda(), roi_1.cuda()

            inputs_1 = inputs_1.unsqueeze(1)
            outImgFeats = net(inputs_1, roi_1)
            outImgFeats = l2Normalize(outImgFeats)
            
            outImgClassScores, outImgEmbed = embedNet(outImgFeats)
            outImgEmbed = l2Normalize(outImgEmbed)
            featImgData = outImgEmbed.cpu().data.numpy()
            
    # to do: for test augmentation
    # if args.featType<=1:
    #     maxFeatMat = np.amax(featImgMat,axis=0)
    # if not(args.featType==1):
    #     maxSynthMat = np.amax(featSynthMat,axis=0)

    return featImgData
