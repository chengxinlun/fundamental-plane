#!/usr/bin/env python
# -*- coding: utf-8 -*-
import core.dataio.specio as s
import core.dataio.rawio as r
import calib.errorcalib as ec


w, f, e = r.get_raw(0, 56660)
w, f, e = ec.errorcalib(w, f, e)
s.save_spec(w, f, e, "data/calib", "0-56660.pkl")
a, b, c = s.get_spec("data/calib/0-56660.pkl")
print(c)
