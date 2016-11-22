#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
core.util.parallel
==================
A module for parallel computation
'''
import multiprocessing as mul

def para_return(func, params, num_thread=4):
    '''
    para_return(func, params, res, num_thread=4)
    ============================================
    Input: func: a function with return
           params: a 2-d list. axis-1 is used to store parameters for func
           num_thread: default value: 4. Number of threads
    '''
    p = mul.Pool(processes=num_thread)
    result = []
    for each in params:
        result.append(p.apply_async(func, each))
    p.close()
    p.join()
    return result
