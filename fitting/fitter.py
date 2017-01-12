#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.fitter
==============
A module for fitter

Note: All functions here must follow the same parameters and same return
'''
from astropy.modeling import fitting
from lmfit.minimizer import Minimizer
from lmfit.parameter import Parameters


__all__ = ['lmlsq']


def lmlsq(model, x, y, e, maxi):
    '''
    lmlsq(model, x, y, initp, maxiter)
    ==================================
    Input: model: A astropy.modeling.models class for the model with initial set
           x: A numpy array for x
           y: A numpy array for y
           e: A numpy array for error of y
           maxi: An int for max number of iterations

    Output: res: A same model with optimized parameters
    '''
    fit = fitting.LevMarLSQFitter()
    res = fit(model, x, y, weights=e**(0.0-2.0), maxiter=maxi)
    return res
