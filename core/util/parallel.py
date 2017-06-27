# -*- coding: utf-8 -*-
'''
core.util.parallel
==================
A module for parallel computation
'''
import multiprocessing as mul


__all__ = ['para_return']


def para_return(func, params, num_thread=4):
    '''
    para_return(func, params, res, num_thread=4)
    ============================================
    Input: func: a function with return
           params: a 2-d list. axis-1 is used to store parameters for func
           num_thread: default value: 4. Number of threads
    '''
    wait_list = []
    res_list = []
    p = mul.Pool(processes=num_thread)
    for each in params:
        r = p.apply_async(func, each)
        wait_list.append(r)
    for each in wait_list:
        res_list.append(each.get())
    p.close()
    p.join()
    return res_list
