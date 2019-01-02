import torch
import cv2
import numpy as np

from scipy.ndimage.interpolation import map_coordinates
from scipy.ndimage.filters import gaussian_filter
from skimage import io, transform

class Normalize(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        image, roi = sample['image'], sample['roi']
        image = (image-np.mean(image)) / ((np.std(image) + 0.0001) / 128.0)

        return {'image': image,
                'roi': roi}


class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        image, roi = sample['image'], sample['roi']

        return {'image': torch.from_numpy(image),
                'roi': torch.from_numpy(roi)}
