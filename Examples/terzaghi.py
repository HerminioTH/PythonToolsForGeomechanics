#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 15:08:02 2018

@author: herminio
"""

from AnalyticalSolutions import Terzaghi
from PhysicalPropertyTools.PropertyParser import Properties
from CGNSTools.CGNSReader import ReadCGNSFile
import pylab as pl




time = 1.0

height = 6.0
tao_0 = 1.0e+5

rock = Properties( "../PhysicalPropertyTools/Json_Files/solid.json" )
fluid = Properties( "../PhysicalPropertyTools/Json_Files/fluid.json" )

terza = Terzaghi.Solution( height, tao_0, rock, fluid )
z_a = terza.getPositionValues()
p_a = terza.getPressureValuesConstTime(time, 400)



g = ReadCGNSFile( "../CGNSTools/Results/Results.cgns" )
    
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