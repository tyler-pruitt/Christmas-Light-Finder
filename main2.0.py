#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 22:21:23 2020

@author: tylerpruitt
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

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
    
def filter_pixel(image, threshold, intensity='same'):
    """
    Filters image by entire pixel, only shows pixels in which all colors exceed of meet threshold.
    
    Parameters
    ----------
    image : array of shape m x n x 3.
    threshold : threashold value in which all values below will be set to 0.
    intensity: uniform value of filtered pixels. default set to same as the input image.

    Returns
    -------
    filter_img : filtered image.
    """
    filter_img = image*0
    print('Filtering with threshold', threshold, '...')
    
    for i in range(len(image)):
        for j in range(len(image[0])):
            red, green, blue = False, False, False
            for k in range(3):
                if image[i][j][k] >= threshold:
                    if k == 0:
                        red = True
                    elif k == 1:
                        green = True
                    else:
                        blue = True
            if red == True and green == True and blue == True:
                if intensity == 'same':
                    filter_img[i][j] = image[i][j]
                elif type(intensity) == int and intensity >= 0 and intensity <= 255:
                    filter_img[i][j] = intensity, intensity, intensity
                else:
                    print('Error: Intensity must be an integer between 0 and 255.')
                    
    return filter_img

def cluster(image, radius=1):
    """
    Clusteres filtered image by clustering around pixels whos neighbors in a square radius all are nonzero.
    
    Parameters
    ----------
    image : filtered image.
    radius : int, square's radius of clustering. The default is 1.

    Returns
    -------
    cluster_img : clustered image.
    count : int, number of clusters.
    """
    rows = len(image)
    columns = len(image[0])
    cluster_img = np.zeros((rows, columns, 3), dtype=int)
    count = 0
    print('Clustering with radius', radius, '...')
    
    for i in range(rows):
        for j in range(columns):
            if image[i][j][0] != 0:
                accept = True
                if i+radius < rows and j+radius < columns and i-radius > -1 and j-radius > -1:
                    for ri in range(-radius,radius+1,1):
                        if accept:
                            for rj in range(-radius,radius+1,1):
                                if cluster_img[i+ri][j+rj][0] != 0:
                                    accept = False
                                    break
                        else:
                            break
                    
                    if accept:
                        cluster_img[i][j] = list(image[i][j])
                        count += 1
    
    return cluster_img, count

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
            if cluster_img[i][j][0] != 0:
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

filtered_img = filter_pixel(img, 230, 255)
plt.imshow(filtered_img)
plt.axis('off')
plt.title('Filtered Image')
plt.show()

clustered_img, cluster_count = cluster(filtered_img, radius=100)
plt.imshow(clustered_img)
plt.axis('off')
plt.title('Clustered Image')
plt.show()

print('cluster count =', cluster_count)

inverse_img = inverse_lights(img, clustered_img, radius=50)
plt.imshow(inverse_img)
plt.axis('off')
plt.title('Where the lights are')
plt.show()

