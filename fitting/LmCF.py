#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.cont
============
A module for continuum model
'''
from lmfit.parameter import Parameters
from lmfit.lineshapes import powerlaw
from .fe2 import Fe2V


__all__ = ['LmCF']


class LmCF():
    def __init__(self, x0, data0, data1, initp=None):
        self.pars = Parameters()
        if initp is None:
            self.pars.add('l1_shift', value=0.0, min=-1000.0, max=1000.0)
            self.pars.add('l1_width', value=500.0)
            self.pars.add('l1_i_r', value=1.0, min=0.0)
            self.pars.add('n3_shift', value=0.0, min=-1000.0, max=1000.0)
            self.pars.add('n3_width', value=500.0)
            self.pars.add('n3_i_r', value=1.0, min=0.0)
            self.pars.add('x0', value=x0, vary=False)
            self.pars.add("amplitude", value=data0, min=0.0)
            self.pars.add('alpha', value=1.0 if data0 < data1 else -1.0)
        else:
            self.pars = initp.deepcopy()

    def eval(self, params, x):
        pvs = params.valuesdict()
        l1s = pvs["l1_shift"]
        l1w = pvs["l1_width"]
        l1i = pvs["l1_i_r"]
        n3s = pvs["n3_shift"]
        n3w = pvs["n3_width"]
        n3i = pvs["n3_i_r"]
        amp = pvs["amplitude"]
        alp = pvs["alpha"]
        x0 = pvs["x0"]
        the = Fe2V.evaluate(x, l1s, l1w, l1i, n3s, n3w, n3i) + powerlaw(x / x0,
                                                                        amp,
                                                                        alp)
        return the

    def residue(self, params, x, data, eps):
        the = self.eval(params, x)
        return (the - data) ** 2.0 / eps
