#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 13:03:11 2018

@author: herminio
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class PlotSlider(object):
    def __init__(self, maskList, timeList):
        self.maskList = maskList
        self.timeList = timeList

        # self.plot()


    def plot(self):
        fig, ax = plt.subplots( 1, 1, figsize=(8,8) )
        plt.subplots_adjust(left=0.08, right=0.97, bottom=0.25)

        lineList = []
        for mask in self.maskList:
            xValues = mask.getXAxisValues(self.timeList[0])
            yValues = mask.getYAxisValues(self.timeList[0])
            line, = ax.plot(xValues, yValues, '-', label=mask.caseName, linewidth=2.0)
            lineList.append( line )

        ax.grid( True, which='both', axis='both', linestyle = '-', color = '#B5B5B5' )
        ax.legend( loc=3, shadow=True, fancybox=True, prop={'size':12} )
        ax.set_xlabel( mask.fieldName, size=14 )
        ax.set_ylabel( mask.axisName, size=14 )

        axcolor = 'lightgoldenrodyellow'
        axTime = plt.axes([0.25, 0.1, 0.65, 0.03])

        sTime = Slider(axTime, 'Time', self.timeList[0], self.timeList[-1], valinit=self.timeList[0])

        def update(val):
            time = self.__findCloser( sTime.val, self.timeList )
            for i, mask in enumerate(self.maskList):
                try:
                    xValues = mask.getXAxisValues(time)
                    yValues = mask.getYAxisValues(time)
                    lineList[i].set_xdata(xValues)
                    lineList[i].set_ydata(yValues)
                except:
                    pass
            fig.canvas.draw_idle()

        sTime.on_changed(update)
        plt.show()




    def __isMiddle( self, vMin, vMax, v ):
        if vMin <= v <= vMax:   return True
        else:                   return False

    def __findCloser( self, value, lista ):
        i = -1
        while 1:
            i += 1
            if self.__isMiddle(lista[i], lista[i+1], value):
                aux1 = abs(value-lista[i])
                aux2 = abs(value-lista[i+1])
                if aux1 < aux2:
                    return round(lista[i], 8)
                else:
                    return round(lista[i+1], 8)







if __name__ == '__main__':
    from AnalyticalSolutions.Terzaghi import Solution
    from PhysicalPropertyTools.PropertyParser import Properties
    from CGNSTools.CGNSReader import ReadCGNSFile, getTol
    from PlotTools import *


    def func( x, y, z ):
        if getTol( x, 0.0 ) and getTol( y, 1.0 ):
            return True
        else:
            return False

    maskList = []

    rock = Properties( "../PhysicalPropertyTools/Json_Files/solid.json" )
    fluid = Properties( "../PhysicalPropertyTools/Json_Files/fluid.json" )
    case1 = Solution( 6.0, 1.0e+5, rock, fluid )
    maskList.append( AnalyticalSolutionMask(case1, 'Y', 'Pressure', 'Analytical Solution', False) )

    case2 = ReadCGNSFile( "../CGNSTools/Results/Results.cgns" )
    case2.loadPointsOfInterest(func)
    case2.sortPointsOfInterest(3)
    maskList.append( NumericalSolutionMask(case2, 'Z', 'Pressure', 'Numerical Solution', False) )


    timeList = maskList[-1].case.time

    slider = PlotSlider(maskList, timeList)
    slider.plot()
