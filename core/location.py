#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
core.location
=============
A module where the directory information of this project is saved
'''
import os


class Location:
    root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../")
    sourcebase = "data/source"
    rawdata = "data/raw"
