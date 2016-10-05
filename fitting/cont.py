#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.cont
============
A module for continuum model

Note: Only derived class of astropy.modeling.Fittable1DModels should be here
'''
from astropy.modeling import models


__all__ = ['ContSdss']


class ContSdss(models.PowerLaw1D + models.Polynomial1D(3)):
    '''
    fitting.cont.ContSdss
    =====================
    PowerLaw1D + Polynomial1D(3)
    '''
