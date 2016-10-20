#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.narrow
==============
A module for narrow line models
'''
from astropy.modeling import models, Fittable1DModel, Parameter
from ..core.util.spectra import v2lambda


__all__ = ['Narrow']


class Narrow(Fittable1DModel):
    '''
    fitting.narrow.Narrow
    =====================
    A unified narrow line model

    Parameters: a, s, w: Amplitude, line shift (km/s) and line width (km/s)
                      c: Theoritical center of narrow line, please fix this
                         parameter
    '''
    inputs = ('x',)
    outputs = ('y',)
    a = Parameter()
    s = Parameter()
    w = Parameter()
    c = Parameter()

    @staticmethod
    def evaluate(x, a, s, w, c):
        res = models.Gaussian1D(a, *v2lambda(s, w, c))
        return res(x)


if __name__ != "__main__":
    pass
