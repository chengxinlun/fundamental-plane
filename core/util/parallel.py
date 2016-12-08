#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
core.util.parallel
==================
A module for parallel computation
'''
import multiprocessing as mul


__all__ = ['para_return']


res_list = []


def _log_result(res):
    res_list.append(res)


def para_return(func, params, num_thread=4):
    '''
    para_return(func, params, res, num_thread=4)
    ============================================
    Input: func: a function with return
           params: a 2-d list. axis-1 is used to store parameters for func
           num_thread: default value: 4. Number of threads
    '''
    p = mul.Pool(processes=num_thread)
    for each in params:
        p.apply_async(func, each, callback=_log_result)
    p.close()
    p.join()
    return res_list
