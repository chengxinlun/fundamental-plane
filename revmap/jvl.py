#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
revmap.jvl
==========
A module for reverberation mapping with Javelin
'''
import os
from ..core.location import Location
from ..core.util.io import create_directory
from javelin.zylc import get_data
from javelin.lcmodel import Cont_Model, Rmap_Model


__all__ = ['rm_single']


def rm_single(rmid, figout, nwalker=300, nchain=150, nburn=150, min_lag=0.0,
              max_lag=200.0, nthread=100.0, ):
    '''
    rm_single(rmid, figout, nwalker=300, nchain=150, nburn=150, min_lag=0.0,
              max_lag=200.0, nthread=100.0)
    ========================================================================
    Input: rmid: rmid for the source
           figout: Output for the figure
           nwalker: default 50, number of walkers
           nchain: default 150, number of chains
           nburn: default 150, number of burning runs
           min_lag: default 0.0, minimum time lag allowed
           max_lag: default 200.0, maximum time lag allowed
           nthread: default 100.0, number of thread used
    '''
    dir_lc = os.path.join(Location.root, Location.lightcurve, str(rmid))
    dir_rm = os.path.join(Location.revmap, str(rmid))
    create_directory(dir_rm)
    dir_rm = os.path.join(Location.root, dir_rm)
    file_co = os.path.join(dir_lc, "cont.txt")
    file_hb = os.path.join(dir_lc, "hbeta.txt")
    file_rm = os.path.join(dir_lc, "rm.txt")
    c = get_data([file_co])
    cmod = Cont_Model(c)
    cmod.do_mcmc(threads=nthread, nwalkers=nwalker, nchains=nchain,
                 nburns=nburn)
    cy = get_data([file_co, file_hb], names=["Continuum", "Hbeta"])
    cy.plot(figout=)
