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
    c_0 = Parameter()
    c_1 = Parameter()
    c_2 = Parameter()
    c_3 = Parameter()

    @staticmethod
    def evaluate(x, amplitude, x_0, alpha, c_0, c_1, c_2, c_3):
        pl = models.PowerLaw1D(amplitude, x_0, alpha, fixed={"x_0": True})
        po = models.Polynomial1D(3)
        po.c0 = c_0
        po.c1 = c_1
        po.c2 = c_2
        po.c3 = c_3
        return pl(x) + po(x)
