#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 21:11:54 2020

@author: tylerpruitt
"""


import numpy as np

def island_finder(matrix, threshold, minIslandSize):
    """
    Finds contiguous regions (or "islands") in a matrix where all values in the island 
    are greater than a threshold (but not necessarily the same).
    

    Parameters
    ----------
    threshold : int or float
        matrix elements must be greater than this value to be a part of
        an island
    minIslandSize : int or float
        min number of connecting (either top, bottom, left or right)
        island elements to constitute an island
    matrix : np.array or some other matrix
        input matrix of arbitrary size

    Returns
    -------
    ans : matrix
    a matrix of same size as input matrix of booleans with islands represented
    by 1's and everything else represented by 0's
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
    
    rows = len(matrix)
    columns = len(matrix[0])
    
    ans = np.zeros( (rows, columns), dtype=int) #create a same sized matrix as input matrix of zeros
    
    for i in range(rows): #loop inserts 1's where values are greater than threshold
        for j in range(columns):
            if matrix[i][j] > threshold:
                ans[i][j] = 1
    
    for i in range(rows): #loop removes 1's which do not satisfy min island size requirements without wrapping edges
        for j in range(columns):
            
            if ans[i][j] == 1: #looking at 1's now
                record = np.zeros( (rows, columns), dtype=bool) #set up record of if position has been searched before
                
                #initializing variables for looking up and down (n) and looking left and right (r) for each i,j pair
                n, r = 0, 0
                
                count = 1 #count i,j position (must count single island first)
                record[i][j] = True #record that position has been counted
                count = upper(count, n, r) #branch out through upper neighbors to i,j position and retrieve count
                count = lower(count, n, r) #feed count back into other branches as previous branch is exhausted
                count = left(count, n, r)
                count = right(count, n, r)
                
                if count < minIslandSize:
                    ans[i][j] = 0
    return ans
