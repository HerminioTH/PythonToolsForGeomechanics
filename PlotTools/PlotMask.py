#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:27:56 2018

@author: herminio
"""

class PlotMask(object):
    def __init__(self, solution, axisName, fieldName, setFielToXAxis=True):
        self.solution = solution
        self.axisName = axisName
        self.fieldName = fieldName
        self.setFielToXAxis = setFielToXAxis
        
    def getXAxisValues(self, time):
        if self.setFieldToXAxis:
            return self.__getFieldValues(time)
        else:
            return self.__getCoordinateValues()
        
    def getYAxisValues(self, time):
        if self.setFieldToXAxis:
            return self.__getCoordinateValues()
        else:
            return self.__getFieldValues(time)
    
    def __getFieldValues(self, time):
        return self.solution.getFieldValuesAtTime(self.fieldName, time)
        
    
    def __getCoordinateValues(self):
        if self.axisName == 'X':
            return self.solution.getCoordinateX()
        elif self.axisName == 'Y':
            return self.solution.getCoordinateY()
        elif self.axisName == 'Z':
            return self.solution.getCoordinateZ()
        else:
            print("Axis not defined!")




if __name__ == '__main__':
    from AnalyticalSolutions import Terzaghi
    from PhysicalPropertyTools.PropertyParser import Properties
    from CGNSTools.CGNSReader import ReadCGNSFile