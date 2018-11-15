#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 15:32:34 2018

@author: herminio
"""

import sys

sys.path.append('../AnalyticalSolutions')
sys.path.append('../PropertyParser')
sys.path.append('../CGNSReader')

from Terzaghi import TerzaghisProblemAnalytical
from PropertyParser import Properties
from CGNSReader import ReadCGNSFile

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

def isMiddle( vMin, vMax, v ):
    if vMin <= v <= vMax:   return True
    else:                   return False
	    
def findCloser( value, lista ):
    i = -1
    while 1:
        i += 1
        if isMiddle(lista[i], lista[i+1], value):
            aux1 = abs(value-lista[i])
            aux2 = abs(value-lista[i+1])
            if aux1 < aux2:
                return round(lista[i], 8)
            else:
                return round(lista[i+1], 8)

def getTol( x, y ):
    if abs(x-y) < 1e-5: return True
    else:               return False

def func( x, y, z ):
    if getTol( x, 0.0 ) and getTol( y, 1.0 ):
        return True
    else:
        return False
    


height = 6.0
tao_0 = 1.0e+5
rock = Properties( "../PropertyParser/Json_Files/solid.json" )
fluid = Properties( "../PropertyParser/Json_Files/fluid.json" )
terza = TerzaghisProblemAnalytical( height, tao_0, rock, fluid )
z_a = terza.getPositionValues()



g = ReadCGNSFile( "../CGNSReader/Results/Results.cgns" )
g.loadPointsOfInterest(func)    
g.sortPointsOfInterest(3)

p_n = g.getFieldValuesAtTime('Pressure', g.time[1])
z_n = g.getCoordinateZ()




## Plot Slider

fig, ax1 = plt.subplots( 1, 1, figsize=(8,8) )
plt.subplots_adjust(left=0.08, right=0.97, bottom=0.25)


line_p_List = []
pMin, pMax = 0., 0.
p_a = np.array(terza.getPressureValuesConstTime( g.time[1], 400, z_a ))
line, = ax1.plot( p_a, z_a, '-', color='black', label='Analytic Solution', linewidth=2.0 )
line_p_List.append( line )

line, = ax1.plot( p_n, z_n, 'o-', label='Numerical Solution', linewidth=2.0 )
line_p_List.append( line )

ax1.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
ax1.legend( loc=3, shadow=True, fancybox=True, prop={'size':12} )
ax1.set_xlabel( 'Pressure (Pa)', size=14 )
ax1.set_ylabel( 'z (m)', size=14 )


axcolor = 'lightgoldenrodyellow'
axTime = plt.axes([0.25, 0.1, 0.65, 0.03])

sTime = Slider(axTime, 'Freq', g.time[1], g.time[-1], valinit=g.time[1])



def update(val):
#    global g.time
    stime = findCloser( sTime.val, g.time )
    p_a = np.array(terza.getPressureValuesConstTime( stime, 400, z_a ))
    line_p_List[0].set_xdata( p_a )
    line_p_List[0].set_ydata( z_a )
    try:
        g.loadPointsOfInterest(func)
        g.sortPointsOfInterest(3)
        z_n = g.getCoordinateZ()
        p_n = g.getFieldValuesAtTime('Pressure', stime)
        line_p_List[1].set_xdata( p_n )
        line_p_List[1].set_ydata( z_n )
    except:
        pass
        
#    for i in range( numberOfGrids ):
#        try:
#            r = r_List[i]
#            r.loadPointsOfInterest( func )
#            y = r.getPointsCoordinates().transpose()[1]
#            p = r.getGridFunctionValuesOnTime( varName, stime )
#            r.Reordenar( y, [p] )
#
#            line_p_List[i+1].set_xdata( np.array(p)/1.e3 )
#            line_p_List[i+1].set_ydata( y )
#        except:
#            pass
    fig.canvas.draw_idle()
    
sTime.on_changed(update)

plt.show()
    