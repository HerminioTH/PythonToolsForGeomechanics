#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 15:08:02 2018

@author: herminio
"""

import pylab as pl
import sys

sys.path.append('../AnalyticalSolutions')
sys.path.append('../PropertyParser')
sys.path.append('../CGNSReader')

from Terzaghi import TerzaghisProblemAnalytical
from PropertyParser import Properties
from CGNSReader import ReadCGNSFile




time = 1.0

height = 6.0
tao_0 = 1.0e+5
rock = Properties( "../PropertyParser/Json_Files/solid.json" )
fluid = Properties( "../PropertyParser/Json_Files/fluid.json" )
terza = TerzaghisProblemAnalytical( height, tao_0, rock, fluid )
z_a = terza.getPositionValues()
p_a = terza.getPressureValuesConstTime(time, 400)



g = ReadCGNSFile( "../CGNSReader/Results/Results.cgns" )
    
def fun(x,y,z):
    if x == 1 and y == 1:
        return True
    else:
        return False

g.loadPointsOfInterest(fun)    
g.sortPointsOfInterest(3)
p_n = g.getFieldValuesAtTime('Pressure', time)
z_n = g.getCoordinateZ()




pl.plot( p_a, z_a, 'b-' )
pl.plot( p_n, z_n, '.-' )
pl.grid(True)
pl.show()