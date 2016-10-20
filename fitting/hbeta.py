#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.hbeta
=============
A module for Hbeta emission line

Note: Only derived class of astropy.modeling.Fittable1DModels should be here
'''
from astropy.modeling import models, Fittable1DModel, Parameter
from ..core.util.spectra import v2lambda


__all__ = ['Hbeta2']


class Hbeta2(Fittable1DModel):
    '''
    fitting.hbeta.Hbeta2
    ====================
    A Hbeta consisted of 2 broad line and 1 narrow line

    Parameters: n_a, n_s, n_w: Amplitude, line shift and line width for narrow
                               line component
                wi_a, wi_s, wi_w: Amplitude, line shift and line width for broad
                                  line components
    '''
    inputs = ('x', )
    outputs = ('y', )
    n_a = Parameter()
    n_s = Parameter()
    n_w = Parameter()
    w1_a = Parameter()
    w1_s = Parameter()
    w1_w = Parameter()
    w2_a = Parameter()
    w2_s = Parameter()
    w2_w = Parameter()

    @staticmethod
    def evaluate(x, n_a, n_s, n_w, w1_a, w1_s, w1_w, w2_a, w2_s, w2_w):
        hc = 4853.41
        res = models.Gaussian1D(n_a, *v2lambda(n_s, n_w, hc)) + \
            models.Gaussian1D(w1_a, *v2lambda(w1_s, w1_w, hc)) + \
            models.Gaussian1D(w2_a, *v2lambda(w2_s, w2_w, hc))
        return res(x)


if __name__ != "__main__":
    pass
