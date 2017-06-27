#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.fitter
==============
A module for fitter

Note: All functions here must follow the same parameters and same return
'''
from astropy.modeling import fitting
from lmfit import Minimizer


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


def conggrad(model, x, y, e, maxi):
    '''
    conggrad(model, x, y, e, maxi)
    ==============================
    Input: model: A class for the model with initial set
           x: A numpy array for x
           y: A numpy array for y
           e: A numpy array for error of y
           maxi: An int for max number of iterations

    Ouput: res: A same model with optimized parameters
    '''
    fitter = Minimizer(model.residue, model.pars, fcn_args=(x, y, e))
    res = fitter.minimize(method='leastsq', params=model.pars)
    return res
