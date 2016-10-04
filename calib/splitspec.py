#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
calib.splitspec
===============
A module for spectra splitting and cutting
'''
import numpy as np


__all__ = ['splitspec']


def _isInrange(x, wrange):
    for each in wrange:
        if min(each) < x and x < max(each):
            return True
    return False


def splitspec(wave, flux, error, wrange):
    '''
    splitspec(wave, flux, error, wrange)
    ====================================
    Input: wave: numpy array for wavelength
           flux: numpy array for flux
           error: numpy array for error
           wrange: 2d numpy array with [:, 1] being the minimum of each range
                   and [:, 2] being the maximum of each range

    Output: wave, flux, error: a list of numpy arrays with each part concacted
    '''
    index = np.where([_isInrange(each, wrange) for each in wave])
    return [wave[index], flux[index], error[index]]
