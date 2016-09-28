#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
core.dataio.specio
==================
A module where spectrum io functions are stored

Note: due to the sacredness of raw data, raw data io functions are stored in
core.dataio.rawio. Further raw data io should also be implemeted there.
'''
import os
import pickle
from ..location import Location
from .rawio import _create_directory


__all__ = ['get_spec', 'save_spec']


def get_spec(filedir):
    f = open(os.path.join(Location.root, filedir), 'rb')
    wave = pickle.load(f)
    flux = pickle.load(f)
    error = pickle.load(f)
    f.close()
    return [wave, flux, error]


def save_spec(wave, flux, error, filedir, filename):
    _create_directory(filedir)
    f = open(os.path.join(Location.root, filedir, filename), 'wb')
    pickle.dump(wave, f)
    pickle.dump(flux, f)
    pickle.dump(error, f)
    f.close()
