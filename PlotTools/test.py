#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 15:45:18 2018

@author: herminio
"""

from AnalyticalSolutions import Terzaghi
from PhysicalPropertyTools.PropertyParser import Properties
from CGNSTools.CGNSReader import ReadCGNSFile, getTol
from PlotTools import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider




def func( x, y, z ):
    if getTol( x, 0.0 ) and getTol( y, 1.0 ):
        return True
    else:
        return False


maskList = []

rock = Properties( "../PhysicalPropertyTools/Json_Files/solid.json" )
fluid = Properties( "../PhysicalPropertyTools/Json_Files/fluid.json" )
case1 = Terzaghi.Solution( 6.0, 1.0e+5, rock, fluid )
maskList.append( AnalyticalSolutionMask(case1, 'Y', 'Pressure', 'Analytical Solution', False) )

case2 = ReadCGNSFile( "../CGNSTools/Results/Results.cgns" )
#case2.loadPointsOfInterest(func)
#case2.sortPointsOfInterest(3)
#maskList.append( NumericalSolutionMask(case2, 'Z', 'Pressure', 'Numerical Solution', False) )
#
#
#timeList = maskList[1].case.time







#
#def isMiddle( vMin, vMax, v ):
#    if vMin <= v <= vMax:   return True
#    else:                   return False
#
#def findCloser( value, lista ):
#    i = -1
#    while 1:
#        i += 1
#        if isMiddle(lista[i], lista[i+1], value):
#            aux1 = abs(value-lista[i])
#            aux2 = abs(value-lista[i+1])
#            if aux1 < aux2:
#                return round(lista[i], 8)
#            else:
#                return round(lista[i+1], 8)
#
#
#fig, ax1 = plt.subplots( 1, 1, figsize=(8,8) )
#plt.subplots_adjust(left=0.08, right=0.97, bottom=0.25)
#
#
#lineList = []
#
#
#for mask in maskList:
#    field = mask.getFieldValues(timeList[0])
#    pos = mask.getCoordinateValues()
#    line, = ax1.plot(field, pos, '-', label=mask.caseName, linewidth=2.0)
#    lineList.append( line )
#    
#
##p_a = np.array(terza.getPressureValuesConstTime( g.time[1], 400, z_a ))
##line, = ax1.plot( p_a, z_a, '-', color='black', label='Analytical Solution', linewidth=2.0 )
##line_p_List.append( line )
##
##line, = ax1.plot( p_n, z_n, 'o-', label='Numerical Solution', linewidth=2.0 )
##line_p_List.append( line )
#
#ax1.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
#ax1.legend( loc=3, shadow=True, fancybox=True, prop={'size':12} )
#ax1.set_xlabel( 'Pressure (Pa)', size=14 )
#ax1.set_ylabel( 'z (m)', size=14 )
#
#axcolor = 'lightgoldenrodyellow'
#axTime = plt.axes([0.25, 0.1, 0.65, 0.03])
#
#sTime = Slider(axTime, 'Time', timeList[0], timeList[-1], valinit=timeList[0])
#
#def update(val):
#    sTime = findCloser( sTime.val, timeList )
#    
#    for i, mask in maskList:
##        try:
#        p = mask.getFieldValues(sTime)
#        pos = mask.getCoordinateValues()
#        lineList[i].set_xdata(p)
#        lineList[i].set_ydata(pos)
##        except:
##            pass
#
#    fig.canvas.draw_idle()
#
#sTime.on_changed(update)
#
#plt.show()














