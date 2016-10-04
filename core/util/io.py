#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
core.util.io
============
A module for non-data related io functions

Note: For data related io, please refer to core.dataio
'''
import os
from ..location import Location


__all__ = ["create_directory"]


def create_directory(dire):
    '''
    create_directory(dire)
    ======================
    Input: dire: a relative directory that needs to be created

    Output: None
    '''
    cwd = os.getcwd()
    os.chdir(Location.root)
    if not os.path.exists(dire):
        os.makedirs(dire)
    os.chdir(cwd)
