#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
core.exception.mjdexception
===========================
A module where functions for mjd related exception is stored

Note: Only derived class of Exception is allowed
'''
__all__ = ['NoSuchDate']


class NoSuchDate(Exception):
    def __init__(self, source, rmid, mjd):
        self.message = "Raised by " + str(source) + ": No such date " + \
            str(mjd) + " in " + str(rmid)

    def __str__(self):
        return str(self.message)
