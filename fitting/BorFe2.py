#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.BorFe2
==============
A module for FeII templates based on Boroson 1994 et al.

Note that it is assumed that FeII will not shift in velocity
'''
import numpy as np
from scipy.interpolate import UnivariateSpline


__all__ = ['borFe2', 'readFe2', 'consFe2']


class borFe2():
    def __init__(self):
        w, f = readFe2()
        self.model = consFe2(w, f)

    def eval(self, x, amp, shift):
        return self.model(x - shift) * amp


def readFe2():
    l = np.loadtxt("irontemplate.dat")
    w = np.power(10.0, l[:, 0])
    f = l[:, 1] * np.power(10.0, 15.0)
    return [w, f]


def consFe2(w, f):
    fet = UnivariateSpline(w, f, s=0)
    return fet
