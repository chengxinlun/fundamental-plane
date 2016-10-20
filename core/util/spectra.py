#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
core.util.spectra
=================
A module for spectra related funtions
'''
import numpy as np


__all__ = ['v2lambda']


def v2lambda(vshift, vwidth, lcenter):
    lwidth = np.sqrt(3.0 / 2.0) * lcenter * vwidth / 299792.458
    lcenter_s = lcenter * (1.0 + vshift / 299792.458)
    return [lwidth, lcenter_s]
