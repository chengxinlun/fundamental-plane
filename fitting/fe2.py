#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
fitting.fe2
===========
A module for FeII templates

Note: Only derived classes of Fittable1DModel are allowed here
'''
import numpy as np
from astropy.modeling import models, Fittable1DModel, Parameter


__all__ = ['Fe2V']


class Fe2V(Fittable1DModel):
    '''
    fitting.fe2.Fe2V
    '''
    inputs = ('x', )
    outputs = ('y', )
    l1_shift = Parameter()
    l1_width = Parameter()
    l1_i_r = Parameter()
    n3_shift = Parameter()
    n3_width = Parameter()
    n3_i_r = Parameter()

    center_l1 = [4026.36, 4093.66, 4178.86, 4258.16, 4278.10, 4296.57, 4303.17,
                 4314.29, 4369.40, 4385.38, 4403.03, 4416.82, 4472.92, 4489.18,
                 4491.40, 4508.28, 4515.34, 4520.22, 4522.63, 4534.17, 4549.47,
                 4555.89, 4563.76, 4576.33, 4582.83, 4583.83, 4589.98, 4595.68,
                 4601.41, 4620.51, 4629.34, 4656.97, 4666.75, 4713.18, 4720.15,
                 4731.44, 4886.93, 4923.92, 5018.45, 5030.64, 5041.06, 5056.35,
                 5132.67, 5154.40, 5169.03, 5188.68, 5197.57, 5234.62, 5238.58,
                 5254.92, 5256.89, 5264.80, 5275.99, 5284.09, 5316.61, 5316.78,
                 5337.71, 5362.86, 5414.09, 5425.27, 5432.98]

    i_l1 = [0.08, 0.06, 0.06, 0.05, 0.08, 0.07, 0.11,
            0.05, 0.10, 0.06, 0.08, 0.09, 0.18, 0.04,
            0.04, 0.12, 0.10, 0.09, 0.09, 0.05, 0.08,
            0.13, 0.11, 0.07, 0.08, 0.08, 0.10, 0.07,
            0.03, 0.10, 0.15, 0.11, 0.12, 0.03, 0.01,
            0.06, 0.06, 0.16, 0.16, 0.10, 0.04, 0.03,
            0.13, 0.10, 0.16, 0.06, 0.13, 0.14, 0.04,
            0.02, 0.02, 0.15, 0.07, 0.11, 0.18, 0.06,
            0.11, 0.08, 0.07, 0.04, 0.08]

    center_n3 = [4003.33, 4053.81, 4063.94, 4068.62, 4076.22, 4114.47, 4122.64,
                 4128.73, 4163.64, 4173.45, 4177.21, 4177.70, 4178.86, 4183.20,
                 4190.96, 4227.17, 4233.17, 4237.57, 4243.97, 4244.81, 4247.24,
                 4259.32, 4276.83, 4287.39, 4296.57, 4303.17, 4305.89, 4314.29,
                 4319.62, 4319.68, 4327.04, 4346.85, 4351.76, 4352.78, 4358.36,
                 4359.12, 4359.34, 4372.43, 4385.38, 4395.03, 4413.78, 4416.27,
                 4421.95, 4432.84, 4443.80, 4450.49, 4452.01, 4452.11, 4457.94,
                 4464.46, 4474.90, 4488.75, 4489.18, 4491.40, 4492.63, 4508.28,
                 4515.34, 4520.22, 4522.63, 4534.17, 4541.52, 4549.47, 4555.89,
                 4576.34, 4582.83, 4583.83, 4616.64, 4620.51, 4629.34, 4634.60,
                 4639.67, 4643.09, 4656.97, 4666.75, 4670.17, 4697.60, 4702.54,
                 4728.07, 4731.44, 4763.79, 4774.72, 4780.60, 4798.27, 4802.61,
                 4814.53, 4824.13, 4836.22, 4874.48, 4876.48, 4889.62, 4893.83,
                 4898.61, 4905.34, 4911.20, 4923.92, 4928.31, 4935.03, 4947.33,
                 4947.37, 4950.74, 4973.39, 4993.35, 5005.51, 5018.43, 5020.23,
                 5072.28, 5101.80, 5111.63, 5158.00, 5158.78, 5161.18, 5169.03,
                 5181.95, 5197.57, 5220.06, 5234.62, 5261.62, 5264.80, 5268.87,
                 5273.35, 5275.99, 5284.08, 5316.61, 5316.78, 5325.56, 5333.65,
                 5362.86, 5370.28, 5376.45, 5379.03, 5412.65, 5425.27, 5432.98,
                 5433.13, 5477.24]

    i_n3 = [0.06, 0.06, 0.06, 0.21, 0.06, 0.05, 0.17,
            0.16, 0.09, 0.44, 0.05, 0.15, 0.15, 0.13,
            0.07, 0.22, 0.58, 0.16, 0.36, 0.08, 0.13,
            0.12, 0.22, 0.38, 0.08, 0.12, 0.06, 0.16,
            0.14, 0.11, 0.26, 0.08, 0.62, 0.10, 0.14,
            0.29, 0.27, 0.07, 0.38, 0.11, 0.19, 0.42,
            0.11, 0.06, 0.32, 0.10, 0.11, 0.12, 0.21,
            0.11, 0.06, 0.08, 0.22, 0.22, 0.06, 0.13,
            0.18, 0.21, 0.29, 0.23, 0.25, 0.28, 0.21,
            0.16, 0.04, 0.37, 0.12, 0.22, 0.61, 0.27,
            0.06, 0.16, 0.13, 0.14, 0.13, 0.05, 0.05,
            0.12, 0.22, 0.16, 0.10, 0.14, 0.02, 0.20,
            0.38, 0.39, 0.28, 0.10, 0.14, 0.13, 0.19,
            0.07, 0.14, 0.17, 0.59, 0.13, 0.19, 0.06,
            0.05, 0.07, 0.08, 0.30, 0.06, 0.45, 0.07,
            0.14, 0.18, 0.06, 0.10, 0.28, 0.18, 0.42,
            0.06, 0.37, 0.05, 0.25, 0.17, 0.11, 0.07,
            0.18, 0.36, 0.26, 0.34, 0.10, 0.15, 0.11,
            0.42, 0.11, 0.09, 0.21, 0.07, 0.22, 0.13,
            0.06, 0.09]

    @staticmethod
    def evaluate(x, l1_shift, l1_width, l1_i_r, n3_shift, n3_width, n3_i_r):
        res = 0.0
        for i in range(0, len(Fe2V.add_modelcenter_l1)):
            f = models.Lorentz1D(l1_i_r * Fe2V.i_l1[i],
                                 Fe2V.center_l1[i] + l1_shift,
                                 l1_width * np.sqrt(3 / 2) * Fe2V.center_l1[i] /
                                 299792.458)
            res = res + f(x)
        for i in range(0, len(Fe2V.center_n3)):
            f = models.Lorentz1D(n3_i_r * Fe2V.i_n3[i],
                                 Fe2V.center_n3[i] + n3_shift,
                                 n3_width * np.sqrt(3 / 2) * Fe2V.center_n3[i] /
                                 299792.458)
            res = res + f(x)
        return res


if __name__ != "main":
    pass
