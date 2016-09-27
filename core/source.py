#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
core.source
===========
A module where a class for basic source information is stored
'''
from psrm.base.target_fibermap import parseVar_sid


class Source:
    rmid = -1
    ra = None
    dec = None
    zfinal = -1
    plate = []
    mjd = []
    fiberid = []
    info_complete = False

    def __init__(self, rmid):
        info = parseVar_sid(rmid, 'ra', 'dec', 'zfinal', 'plate', 'mjd',
                            'fiberid')
        self.ra = info[rmid]['ra']
        self.dec = info[rmid]['dec']
        self.zfinal = info[rmid]['zfinal']
        self.rmid = rmid
        self.plate = info[rmid]['plate']
        self.mjd = info[rmid]['mjd']
        self.fiberid = info[rmid]['fiberid']
        self.info_complete = True

    def __str__(self):
        return "Source Rmid: " + str(self.rmid) + "\n" + \
            "    RA, DEC: " + str(self.ra) + ", " + str(self.dec) + "\n" + \
            "     Zfinal: " + str(self.zfinal)
