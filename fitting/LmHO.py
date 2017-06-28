#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.LmHO
=============
A module for Hbeta and OIII emission line
'''
from lmfit.parameter import Parameters
from lmfit.lineshapes import gaussian
from ..core.util.spectra import v2lambda


__all__ = ['LmHO']


class LmHO():
    '''
    fitting.hbeta.Hbeta2
    ====================
    A Hbeta consisted of 2 broad line and 1 narrow line

    Parameters: n_a, n_s, n_w: Amplitude, line shift and line width for narrow
                               line component
                wi_a, wi_s, wi_w: Amplitude, line shift and line width for broad
                                  line components
    '''
    def __init__(self, initp=None):
        self.pars = Parameters()
        if initp is None:
            # O3
            self.pars.add('o3amp1', value=20.0, min=0.0)
            self.pars.add('o3amp2', value=20.0, min=0.0)
            self.pars.add('o3shift', value=0.0, min=-1000.0, max=1000.0)
            self.pars.add('o3width', value=20.0, min=0.0)
            # Hbeta narrow
            self.pars.add('hnamp', value=10.0, min=0.0)
            self.pars.add('hnshift', value=0.0, min=-1000.0, max=1000.0)
            self.pars.add('hnwidth', value=500.0, min=100.0, max=1200.0)
            # Hbeta broad
            self.pars.add('hbamp1', value=40.0, min=0.0)
            self.pars.add('hbamp2', value=40.0, min=0.0)
            self.pars.add('hbshift1', value=0.0, min=-1000.0, max=1000.0)
            self.pars.add('hbshift2', value=0.0, min=-1000.0, max=1000.0)
            self.pars.add('hbwidth1', value=1500.0, min=1200.0, max=2000.0)
            self.pars.add('hbwidth2', value=1500.0, min=1200.0, max=2000.0)
        else:
            self.pars = initp.deepcopy()

    def eval(self, params, x):
        hb = 4853.41
        hn = 4853.41
        o1 = 5008.22
        o2 = 4960.36
        pvs = params.valuesdict()
        o3a1 = pvs["o3amp1"]
        o3a2 = pvs["o3amp2"]
        o3s = pvs["o3shift"]
        o3w = pvs["o3width"]
        hna = pvs["hnamp"]
        hns = pvs["hnshift"]
        hnw = pvs["hnwidth"]
        hba1 = pvs["hbamp1"]
        hba2 = pvs["hbamp2"]
        hbs1 = pvs["hbshift1"]
        hbs2 = pvs["hbshift2"]
        hbw1 = pvs["hbwidth1"]
        hbw2 = pvs["hbwidth2"]
        the = gaussian(x, o3a1, *v2lambda(o3s, o3w, o1)) + \
            gaussian(x, o3a2, * v2lambda(o3s, o3w, o2)) + \
            gaussian(x, hna, * v2lambda(hns, hnw, hn)) + \
            gaussian(x, hba1, * v2lambda(hbs1, hbw1, hb)) + \
            gaussian(x, hba2, * v2lambda(hbs2, hbw2, hb))
        return the

    def residue(self, params, x, data, eps):
        the = self.eval(params, x)
        return ((the - data) / eps) ** 2.0

    def integrate(self, params):
        pvs = params.valuesdict()
        o3a1 = pvs["o3amp1"]
        o3a2 = pvs["o3amp2"]
        hna = pvs["hnamp"]
        hba1 = pvs["hbamp1"]
        hba2 = pvs["hbamp2"]
        res_dict = {"o3": o3a1 + o3a2, "hbeta": hna + hba1 + hba2}
        return res_dict
