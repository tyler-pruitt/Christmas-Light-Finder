#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 09:38:43 2021

@author: tylerpruitt
"""

import numpy as np
import random

def island_cluster(matrix, maxIslandSize=1, isRandom=False):
    """
    Counts the number of contiguous regions (or "islands") or clusters in a matrix.
    Clusters together or shrinks clusters to the size of the element.
    At the moment, maxIslandSize does nothing since it would affect islandCount and the clustering of other originally separate islands.

    Parameters
    ----------
    matrix : np.array or any other matrix
        A matrix of contiguous regions (or "islands") where all values in the island 
    are greater than a threshold (but not necessarily the same). Island elements are represented by 1, non-island elements are represented by 0.
    maxIslandSize : int, optional
        The number of elements set to represent the island after clustering. If number of elements is less than maxIslandSize, it will be the number of elements in the island. The default is 1.
    isRandom : bool, optional
        If set to True, a random element in the island is chosen to represent the island, instead of the top left most element. The default is False.

    Returns
    -------
    ans : np.array
        A matrix of clustered islands with every island represented by at least one element.
    islandCount : int
        The number of contiguous regions (or "islands") in a matrix.

    """
    #create some helper functions
    
    def upper(count, n, r):
        """
        searches above previous matrix position by decreasing n by 1
        """
        if i+n != 0: #if not an upper edge
            if ans[i-1+n][j+r] == 1 and record[i-1+n][j+r] == False: #if upper is 1 and not seached before
                count += 1
                record[i-1+n][j+r] = True #record that position has been counted before for this i, j pair
                count = upper(count, n-1, r) #feed count back into branches
                count = left(count, n-1, r)
                count = right(count, n-1, r)
        return count
    
    def lower(count, n, r):
        """
        searches below previous matrix position by increasing n by 1
        """
        if i+n != rows - 1: #if not a lower edge
            if ans[i+1+n][j+r] == 1 and record[i+1+n][j+r] == False: #if lower is 1 and not searched before
                count += 1
                record[i+1+n][j+r] = True #record that position has been counted before for this i, j pair
                count = lower(count, n+1, r) #feed count back into branches
                count = left(count, n+1, r)
                count = right(count, n+1, r)
        return count
    
    def left(count, n, r):
        """
        searches to the left of previous matrix position by decreasing r by 1
        """
        if j+r != 0: #if not a left edge
            if ans[i+n][j-1+r] == 1 and record[i+n][j-1+r] == False: #if left is 1 and not searched before
                count += 1
                record[i+n][j-1+r] = True #record that position has been counted before for this i, j pair
                count = upper(count, n, r-1) #feed count back into branches
                count = lower(count, n, r-1)
                count = left(count, n, r-1)
        return count
    
    def right(count, n, r):
        """
        searches to the right of previous matrix position by increasing r by 1
        """
        if j+r != columns - 1: #if not an edge
            if ans[i+n][j+1+r] == 1 and record[i+n][j+1+r] == False: #if right is 1 and not searched before
                count += 1
                record[i+n][j+1+r] = True #record that position has been counted before for this i, j pair
                count = upper(count, n, r+1) #feed count back into branches
                count = lower(count, n, r+1)
                count = right(count, n, r+1)
        return count
    
    """
    if maxIslandSize < 1 or maxIslandSize > count:
        raise ValueError
    """
    
    rows = len(matrix)
    columns = len(matrix[0])
    
    ans = np.zeros( (rows, columns), dtype=int)
    
    for i in range(rows):
        for j in range(columns):
            ans[i][j] = matrix[i][j]
    
    for i in range(rows):
        for j in range(columns):
            if ans[i][j] != 0:
                record = np.zeros( (rows, columns), dtype=bool)
                
                #initializing variables for looking up and down (n) and looking left and right (r) for each i,j pair
                n, r = 0, 0
                
                count = 1 #count i,j position (must count single island first)
                record[i][j] = True #record that position has been counted
                count = upper(count, n, r) #branch out through upper neighbors to i,j position and retrieve count
                count = lower(count, n, r) #feed count back into other branches as previous branch is exhausted
                count = left(count, n, r)
                count = right(count, n, r)
                
                if isRandom:
                    randRow = random.randrange(len(record))
                    randCol = random.randrange(len(record[randRow]))
                    
                    while record[randRow][randCol] == False:
                        randRow = random.randrange(len(record))
                        randCol = random.randrange(len(record[randRow]))
                    
                    for m in range(rows):
                        for n in range(columns):
                            if record[m][n] == True and (m != randRow or n != randCol):
                                ans[m][n] = 0
                                record[m][n] = False
                else:
                    for m in range(rows):
                        for n in range(columns):
                            if record[m][n] == True and (m != i or n != j):
                                ans[m][n] = 0
                                record[m][n] = False
    
    islandCount = 0
    
    for i in range(rows):
        for j in range(columns):
            if ans[i][j] != 0:
                islandCount += 1
    
    return ans, islandCount