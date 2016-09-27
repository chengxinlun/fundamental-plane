#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
core.dataio.rawio
=================
A module where functions related to raw data input and output are stored
'''
import os
import pickle
import numpy as np
from psrm.analSpec.ob2rf import ob2rf
from psrm.analSpec.deredden import SF_deredden
from ..source import Source
from ..location import Location


def get_source_info(rmid):
    '''
    get_source_info(rmid)
    ==================
    Input: rmid: rmid of the source

    Output: info: a core.source.Source class with information about the source
    '''
    fname = str(rmid) + ".pkl"
    try:
        # Find information in Source class
        f = open(os.path.join(Location.root, Location.sourcebase, fname), "rb")
        info = pickle.load(f)
        f.close()
    except Exception:
        # If Source class cannot be found, create one
        info = Source(rmid)
        try:
            _create_directory(Location.sourcebase)
            # Save it to file
            fo = open(os.path.join(Location.root, Location.sourcebase, fname),
                      "wb")
            pickle.dump(info, fo)
            fo.close()
        except Exception:
            # If save encounter failure, ignore
            pass
    return info


def get_raw(rmid, mjd):
    '''
    get_raw(rmid, mjd)
    =================
    Input: rmid: rmid of the source object
            mjd: modified julian date

    Output: wave: a numpy array with wavelength
            flux: a numpy array with flux
            error: a numpy array with error of the flux
    '''
    fname = str(rmid) + "-" + str(mjd) + ".pkl"
    try:
        # Get pickled database
        f = open(os.path.join(Location.root, Location.rawdata, fname), "rb")
        wave, flux, error = pickle.load(f)
        f.close()
    except Exception:
        # If cannot find pickled data, read and pickle
        wave, flux, error = _get_raw_nofile(rmid, mjd)
        try:
            _create_directory(Location.rawdata)
            fo = open(os.path.join(Location.root, Location.rawdata, fname),
                      "wb")
            pickle.dump(wave, fo)
            pickle.dump(flux, fo)
            pickle.dump(error, fo)
            fo.close()
        except Exception:
            pass
    return [wave, flux, error]


def _get_raw_nofile(rmid, mjd):
    info = get_source_info(rmid)
    if not info.info_complete:
        raise Exception("Information about source " + str(rmid) +
                        " is incomplete")
    if not (mjd in info.mjd):
        raise Exception("The source " + str(rmid) + " does not have data on " +
                        str(mjd))
    zfinal = info.zfinal
    # Get the corresponding plate, fiberid
    index = np.where(info.mjd == mjd)[0]
    plate = info.plate[index]
    fiberid = info.fiberid[index]
    # Read data from fits (Reference: psrm.plotSpec.plotSPec)
    parM = SF_deredden(plate, fiberid, 'fluxerr', mjd=mjd)
    wave = parM['wave']
    flux = parM['flux']
    error = parM['fluxerr']
    rf = ob2rf(wave, flux, zfinal, fluxerr=error)
    return [rf["wave"], rf["flux"], rf["fluxerr"]]


def _create_directory(dire):
    cwd = os.getcwd()
    os.chdir(Location.root)
    if not os.path.exists(dire):
        os.makedirs(dire)
    os.chdir(cwd)
