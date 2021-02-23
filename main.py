#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 20:17:49 2020
Last updated on Mon Feb 22 20:50:29 2021
Version 3.0

@author: tylerpruitt
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

from islandFinder import island_finder
from islandCluster import island_cluster

def single_color(image, color, negative=False):
    """
    Parameters
    ----------
    image : array of shape m x n x 3.
    color : int; 0=red, 1=green, 2=blue.
    value : threashold value in which all values below will be set to 0.
    negative : boolean; if True returns the negative of the filtered image; default set to False.

    Returns
    -------
    filter_image : filtered image.
    """
    filter_image = image*0
    if negative == True:
        filter_image[:,:,color] = 255 - image[:,:,color]
    elif negative == False:
        filter_image[:,:,color] = image[:,:,color]
    else:
        print('Error with parameter negative: negative must be a boolean.')
        
    return filter_image

def inverse_lights(image, cluster_img, radius=1):
    """
    Returns the original image with black boxes covering where the program believes the lights are.
    
    Parameters
    ----------
    image : original image.
    cluster_img : clustered image.
    radius : int, radius of black boxes(squares). The default is 1.

    Returns
    -------
    inv_img : original image with black boxes (squares of a given radius) covering lights.
    """
    rows = len(image)
    columns = len(image[0])
    inv_img = 1*image
    
    for i in range(rows):
        for j in range(columns):
            if cluster_img[i][j][1] != 0:
                for ri in range(-radius,radius+1,1):
                    for rj in range(-radius,radius+1,1):
                        inv_img[i+ri][j+rj] = 0,0,0
    
    return inv_img

try:
    img = plt.imread(sys.argv[1])
except:
    img =plt.imread('Christmas.jpg')

plt.figure(frameon=False)
plt.imshow(img)
plt.axis('off')
plt.show()

plt.figure(frameon=False)
red_img = single_color(img, color=0)
plt.imshow(red_img)
plt.axis('off')
plt.show()

plt.figure(frameon=False)
green_img = single_color(img, color=1)
plt.imshow(green_img)
plt.axis('off')
plt.show()

plt.figure(frameon=False)
blue_img = single_color(img, color=2)
plt.imshow(blue_img)
plt.axis('off')
plt.show()

minPixelThreshold = int(input('Enter pixel threshold on the 255 scale: '))
islandSize = int(input('Enter minimum island size for ligts: '))

print('Finding islands with threshold', minPixelThreshold, 'and minimum island size', islandSize, '...')
filtered_green = island_finder(green_img[:,:,1], minPixelThreshold, islandSize)
print('Done.')

print('Clustering and counting islands ...')
clustered_green, cluster_count = island_cluster(filtered_green)
print('Done.')

print('Number of lights:', cluster_count)

clustered_green_img = np.zeros((len(img), len(img[0]), 3), dtype=int)
clustered_green_img[:,:,1] = filtered_green

inverse_img = inverse_lights(img, clustered_green_img, radius=50)
plt.imshow(inverse_img)
plt.axis('off')
plt.title('Where the lights are')
plt.show()

