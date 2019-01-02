import math
#from collections import OrderedDict
import torch.nn as nn
import torch.nn.init as init
import torch as th
import torch.nn.functional as F
from torch.autograd import Variable
import math
import pdb

class SPPLayer(nn.Module):

    def __init__(self, num_levels=3, pool_type='max_pool'):
        super(SPPLayer, self).__init__()

        self.num_levels = num_levels
        self.pool_type = pool_type

    def forward(self, x):
        bs, c, h, w = x.size()
        if w<9:
            #print('Warning:Padding--Check')
            padLayer = nn.ReplicationPad2d((0, 9-w, 0, 0))
            x = padLayer(x)
            bs, c, h, w = x.size()
        pooling_layers = []
        for i in range(self.num_levels):
            #kernel_size = w // (2 ** i)
            kernel_size = w // (i+1)
            #kernel_size = int(math.ceil(w/(i+1)))
            if self.pool_type == 'max_pool':
                tensor = F.max_pool2d(x, kernel_size=(h,kernel_size),
                                      stride=kernel_size).view(bs, -1)
            else:
                tensor = F.avg_pool2d(x, kernel_size=(h,kernel_size),
                                      stride=kernel_size).view(bs, -1)

            pooling_layers.append(tensor)
        x = th.cat(pooling_layers, dim=-1)

        return x
