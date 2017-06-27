#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.LmCF
============
A module for continuum and optical FeII model
'''
from lmfit.parameter import Parameters
from lmfit.lineshapes import powerlaw
from .BorFe2 import borFe2


__all__ = ['LmCF']


class LmCF():
    def __init__(self, x0, data0, data1, initp=None):
        self.pars = Parameters()
        if initp is None:
            self.pars.add('fe2amp', value=1.0, min=0.0)
            self.pars.add('fe2shift', value=0.0, min=-100.0, max=100.0)
            self.pars.add('x0', value=x0, vary=False)
            self.pars.add("amplitude", value=data0, min=0.0)
            self.pars.add('alpha', value=1.0 if data0 < data1 else -1.0)
        else:
            self.pars = initp.deepcopy()
        self.fet = borFe2()

    def eval(self, params, x):
        pvs = params.valuesdict()
        feamp = pvs["fe2amp"]
        feshift = pvs["fe2shift"]
        amp = pvs["amplitude"]
        alp = pvs["alpha"]
        x0 = pvs["x0"]
        the = powerlaw(x / x0, amp, alp) + self.fet.eval(x, feamp, feshift)
        return the

    def residue(self, params, x, data, eps):
        the = self.eval(params, x)
        return ((the - data) / eps) ** 2.0
