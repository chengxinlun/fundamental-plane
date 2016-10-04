#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
calib.ptcalib
=============
A module where functions for p(t) calibration is involved

Note: This section only reads the data from PrepSpec, and use it to calibrate.
For futher detail of this procedure, please refer to Shen et al. 2015
'''
import os
import numpy as np
from ..core.location import Location
from ..core.dataio.rawio import get_source_info, get_raw
from ..core.exception import mjdexception


__all__ = ['ptcalib']


def _read_p0(rmid, mjd_offset=50000.0-0.02):
    # mjd_offset is used to unify the mjd from psrm and sdss's data
    filedir = "rm" + '{:0>3}'.format(int(rmid))
    filename = filedir + "_p0_t.dat"
    data = np.loadtxt(os.path.join(Location.root, Location.pt, filedir,
                                   filename))
    mjd = np.rint(data[:, 0] + np.repeat([mjd_offset], [len(data[:, 0])]))
    p0 = data[:, 1]
    err = data[:, 2]
    return [mjd, p0, err]


def ptcalib(rmid, mjd):
    '''
    ptcalib(rmid)
    =============
    Input: rmid: rmid of source
           mjd: modified julian date

    Output: wave: a numpy array of wavelength
            flux: a numpy array of flux
            error: a numpy array of error
    '''
    mjdlist, p0, err = _read_p0(rmid)
    s = get_source_info(rmid)
    if mjd not in s.mjd:
        raise mjdexception.NoSuchDate("Source", rmid, mjd)
    if mjd not in np.rint(mjdlist):
        raise mjdexception.NoSuchDate("Pt", rmid, mjd)
    index = np.where(mjdlist == mjd)
    c_p0 = p0[index][0]
    c_p0_err = err[index][0]
    pt = np.exp(c_p0)
    pt_err = pt * c_p0_err
    wave, flux, error = get_raw(rmid, mjd)
    error = error * pt + flux * pt_err
    flux = flux * pt
    return [wave, flux, error]
