#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
calib.errorcalib
================
A module where functions of calibration for error = 0 is stored
'''
import numpy as np


__all__ = ['errorcalib']


def errorcalib(wave, flux, error):
    '''
    errorcalib(wave, flux, error)
    =============================
    Input: wave: a numpy array with wavelength
           flux: a numpy array with flux
           error: a numpy array with error

    Output: cal: a list with only none-zero error points of wave, flux, error
    '''
    none_zero_error = np.nonzero(error)
    cal = [wave[none_zero_error], flux[none_zero_error], error[none_zero_error]]
    return cal
