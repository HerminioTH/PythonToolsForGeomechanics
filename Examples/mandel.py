#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 17:52:35 2018

@author: herminio
"""

from AnalyticalSolutions import Mandel
from PhysicalPropertyTools.PropertyParser import Properties
from CGNSTools.CGNSReader import ReadCGNSFile
import pylab as pl


lenght = 5.0
height = 1.0
Force = 5.0e+7

rock = Properties( "../PhysicalPropertyTools/Json_Files/solid.json" )
fluid = Properties( "../PhysicalPropertyTools/Json_Files/fluid.json" )

mandel = Mandel.Solution( lenght, height, Force, rock, fluid )
x = mandel.getXPositionValues();
y = mandel.getYPositionValues();

time = [10., 1000., 10000., 50000., 100000., 500000.]

for t in time:
    p = mandel.getPressureValuesConstTime(t, x)
    pl.plot(x, p)
pl.grid(True)
pl.show()