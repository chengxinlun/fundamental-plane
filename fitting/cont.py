#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.cont
============
A module for continuum model

Note: Only derived class of astropy.modeling.Fittable1DModels should be here
'''
from astropy.modeling import models, Fittable1DModel, Parameter


__all__ = ['ContSdss']


class ContSdss(Fittable1DModel):
    '''
    fitting.cont.ContSdss
    =====================
    PowerLaw1D + Polynomial1D(3)
    '''
    inputs = ('x', )
    outputs = ('y', )
    amplitude = Parameter()
    x_0 = Parameter()
    alpha = Parameter()

    @staticmethod
    def evaluate(x, amplitude, x_0, alpha):
        pl = models.PowerLaw1D(amplitude, x_0, alpha, fixed={"x_0": True})
        return pl(x)
