'''LeNet in PyTorch.'''
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from .sppNet import SPPLayer
import pdb

class hwnetSynthSPP(nn.Module):
    def __init__(self, spp_level, num_classes=10000, phocVecSize=5853):
        super(hwnetSynthSPP,self).__init__()

        self.conv1 = nn.Conv2d(1, 64, 5)
        self.bn1 = nn.BatchNorm2d(64)
        self.pool1 = nn.MaxPool2d(2, 2)

        self.conv2 = nn.Conv2d(64, 128, 5, padding=2)
        self.bn2 = nn.BatchNorm2d(128)
        self.pool2 = nn.MaxPool2d(2, 2)

        self.conv3 = nn.Conv2d(128, 256, 3, padding=1)
        self.bn3 = nn.BatchNorm2d(256)

        self.conv4 = nn.Conv2d(256, 512, 3, padding=1)
        self.bn4 = nn.BatchNorm2d(512)
        self.pool4 = nn.MaxPool2d(2, 2)

        self.conv5 = nn.Conv2d(512, 512, 3, padding=1)
        self.bn5 = nn.BatchNorm2d(512)

        self.spp_layer = SPPLayer(spp_level)

        #self.fc1 = nn.Linear(512*6*12, 2048)
        self.fc1 = nn.Linear(3072, 2048)
        self.bn6 = nn.BatchNorm1d(2048)

        self.fc2 = nn.Linear(phocVecSize+2048, 2048)
        self.bn7 = nn.BatchNorm1d(2048)
        #
        # self.fc3 = nn.Linear(2048,num_classes)

        # #Weight Initialization
        # for m in self.modules():
        #     if isinstance(m, nn.Conv2d):
        #         n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
        #         m.weight.data.normal_(0, math.sqrt(2. / n))
        #     elif isinstance(m, nn.BatchNorm2d):
        #         m.weight.data.fill_(1)
        #         m.bias.data.zero_()
        #     elif isinstance(m, nn.BatchNorm1d):
        #         m.weight.data.fill_(1)
        #         m.bias.data.zero_()
        #     elif isinstance(m, nn.Linear):
        #         n = m.in_features * m.out_features
        #         m.weight.data.normal_(0, math.sqrt(2. / n))

    def resetLastLayer(self, num_classes):
        self.fc3 = nn.Linear(2048,num_classes)
        n = self.fc3.in_features * self.fc3.out_features
        self.fc3.weight.data.normal_(0, math.sqrt(2. / n))

    def forward(self, x, roi, phocTensor):
        out = F.pad(x,(2,2,2,2),mode='replicate')
        out = self.pool1(F.relu(self.bn1(self.conv1(out))))
        out = self.pool2(F.relu(self.bn2(self.conv2(out))))
        out = F.relu(self.bn3(self.conv3(out)))
        out = self.pool4(F.relu(self.bn4(self.conv4(out))))
        out = F.relu(self.bn5(self.conv5(out)))

        # out = self.roi_pooling(out, roi, size=(6,12), spatial_scale=1.0/8)

        # out = out.view(-1,512*6*12)
        out = self.roi_spp_pooling(out, roi, size=(6,12), spatial_scale=1.0/8)

        #out = out.view(-1,512*6*12)
        out = out.view(-1,3072)


        out = F.relu(self.bn6(self.fc1(out)))

        #appending phoc tensor here or before ????
        out = torch.cat((out,phocTensor),1)
        out = F.relu(self.bn7(self.fc2(out)))

        return out

    def roi_pooling(self, input, rois, size=(7,7), spatial_scale=1.0):

        assert(rois.dim() == 2)
        assert(rois.size(1) == 5)
        output = []
        rois = rois.data.float()
        num_rois = rois.size(0)

        rois[:,1:].mul_(spatial_scale)
        rois = rois.long()
        for i in range(num_rois):
            roi = rois[i]
            im_idx = roi[0]
            im = input.narrow(0, im_idx, 1)[..., roi[2]:(roi[4]+1), roi[1]:(roi[3]+1)]
            output.append(F.adaptive_max_pool2d(im, size))

        return torch.cat(output, 0)

    def roi_spp_pooling(self, input, rois, size=(7,7), spatial_scale=1.0):
        #size param not used.

        assert(rois.dim() == 2)
        assert(rois.size(1) == 5)
        output = []
        rois = rois.data.float()
        num_rois = rois.size(0)
        origROIs = rois.clone()
        rois[:,1:].mul_(spatial_scale)
        rois = rois.long()
        for i in range(num_rois):
            roi = rois[i]
            im_idx = roi[0]
            im = input.narrow(0, im_idx, 1)[..., roi[2]:(roi[4]+1), roi[1]:(roi[3]+1)]
            # if(im.size()[3]<9):
            #     print('Warning:ROI size less than 9--Check')
            #output.append(F.adaptive_max_pool2d(im, size))
            output.append(self.spp_layer(im))
        return torch.cat(output, 0)
