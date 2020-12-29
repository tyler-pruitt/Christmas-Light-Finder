#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 21:11:54 2020

@author: tylerpruitt
"""


"""
Write a function, in the programming language of your choice, 
which finds contiguous regions (or "islands") in a matrix where 
all values in the island are greater than a threshold 
(but not necessarily the same). The function should take a threshold, 
a minimum island size, and an arbitrarily sized matrix as inputs. 
The function should output a matrix (same size as the input matrix) 
of booleans. Do not wrap around matrix edges. Corner neighbors are 
not sufficient for island continuity. For example, if the the inputs 
are: threshold = 5, min island size = 3, and 
matrix = [4, 4, 4, 2, 2; 4, 2, 2, 2, 2; 2, 2, 8, 7, 2; 
2, 8, 8, 8, 2; 8, 2, 2, 2, 8]. 
Then the output would be [0, 0, 0, 0, 0; 0, 0, 0, 0, 0; 0, 0, 1, 1, 0;
 0, 1, 1, 1, 0; 0, 0, 0, 0, 0].
"""

import numpy as np

def island_finder(threshold, minislandsize, matrix):
    """
    inputs: threshold and minislandsize are nums
    
            threshold = matrix elements must be greater than this value to be a part of
            an island
            
            minislandsize = min number of connecting (either top, bottom, left or right)
            island elements to constitute an island
            
            matrix = input matrix of arbitrary size
    
    returns: a matrix of same size as input matrix of booleans with islands represented
    by 1's and everything else represented by 0's
    """
    rows = len(matrix)
    columns = len(matrix[0])
    ans = np.zeros( (rows, columns), dtype=int) #create a same sized matrix as input matrix of zeros
    for i in range(rows): #loop inserts 1's where values are greater than threshold
        for j in range(columns):
            if matrix[i][j] > threshold:
                ans[i][j] = 1
    for i in range(rows): #loop removes 1's which do not satisfy min island size requirements without wrapping edges
        for j in range(columns):
            record = np.zeros( (rows, columns), dtype=bool) #set up record of if position has been searched before
            #initializing variables for looking up and down (n) and looking left and right (r) for each i,j pair
            n = 0
            r = 0
            def upper(count, n, r): #searches above previous matrix position by decreasing n by 1
                if i+n != 0: #if not an upper edge
                    if ans[i-1+n][j+r] == 1 and record[i-1+n][j+r] == False: #if upper is 1 and not seached before
                        count += 1
                        record[i-1+n][j+r] = True #record that position has been counted before for this i, j pair
                        (count, n1, r1) = upper(count, n-1, r) #feed count back into branches
                        (count, n2, n2) = left(count, n-1, r)
                        (count, n3, r3) = right(count, n-1, r)
                return (count, n, r)
            def lower(count, n, r): #searches below previous matrix position by increasing n by 1
                if i+n != rows - 1: #if not a lower edge
                    if ans[i+1+n][j+r] == 1 and record[i+1+n][j+r] == False: #if lower is 1 and not searched before
                        count += 1
                        record[i+1+n][j+r] = True #record that position has been counted before for this i, j pair
                        (count, n1, r1) = lower(count, n+1, r) #feed count back into branches
                        (count, n2, r2) = left(count, n+1, r)
                        (count, n3, r3) = right(count, n+1, r)
                return (count, n, r)
            def left(count, n, r): #searches to the left of previous matrix position by decreasing r by 1
                if j+r != 0: #if not a left edge
                    if ans[i+n][j-1+r] == 1 and record[i+n][j-1+r] == False: #if left is 1 and not searched before
                        count += 1
                        record[i+n][j-1+r] = True #record that position has been counted before for this i, j pair
                        (count, n1, r1) = upper(count, n, r-1) #feed count back into branches
                        (count, n2, r2) = lower(count, n, r-1)
                        (count, n3, r3) = left(count, n, r-1)
                return (count, n, r)
            def right(count, n, r): ##searches to the right of previous matrix position by increasing r by 1
                if j+r != columns - 1: #if not an edge
                    if ans[i+n][j+1+r] == 1 and record[i+n][j+1+r] == False: #if right is 1 and not searched before
                        count += 1
                        record[i+n][j+1+r] = True #record that position has been counted before for this i, j pair
                        (count, n1, r1) = upper(count, n, r+1) #feed count back into branches
                        (count, n2, r2) = lower(count, n, r+1)
                        (count, n3, r3) = right(count, n, r+1)
                return (count, n, r)
            if ans[i][j] == 1: #looking at 1's now
                count = 1 #count i,j position (must count single island first)
                record[i][j] = True #record that position has been counted
                (count, n1 ,r1) = upper(count, n, r) #branch out through upper neighbors to i,j position and retrieve count
                (count, n2, r2) = lower(count, n, r) #feed count back into other branches as previous branch is exhausted
                (count, n3, r3) = left(count, n, r)
                (count, n4, r4) = right(count, n, r)
                if count < minislandsize:
                    ans[i][j] = 0
    return ans
