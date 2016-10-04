#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
visual.plotspec
===============
A module where the function for plotting spectrum is stored
'''
import os
import matplotlib.pyplot as plt
from ..core.location import Location
from ..core.util.io import create_directory


def plotspec(wave, flux, error=None, filedir=None, filename=None, **kwargs):
    '''
    plotspec(wave, flux, error, filename, **kwargs)
    ===============================================
    Input: wave: a numpy array for wave length
           flux: a numpy array for wave length
           error: default None, a numpy array for error, leave as None if error
                  bars should not be included in the plot
           filename: default None, relative directory for plot storage, leave as
                     None if the plot should be shown instead of saved
           **kwargs(optional): optional arguments for matplotlib

    Output: None
    '''
    if error is not None:
        plt.errorbar(wave, flux, yerr=error, **kwargs)
    else:
        plt.plot(wave, flux, **kwargs)
    if (filename is not None) and (filedir is not None):
        f = os.path.join(Location.root, filedir, filename)
        create_directory(filedir)
        plt.savefig(f)
    else:
        plt.show()
    plt.close()
