#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 13:41:12 2018

@author: herminio
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from abc import ABC, abstractmethod

class SolutionMask(ABC):
    def __init__(self, case, axisName, fieldName, caseName, setFieldToXAxis=True):
        self.case = case
        self.axisName = axisName
        self.fieldName = fieldName
        self.caseName = caseName
        self.setFieldToXAxis = setFieldToXAxis
        super(SolutionMask, self).__init__()
        
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
    
    @abstractmethod
    def getFieldValues(self, time):
        pass
    
    @abstractmethod
    def getCoordinateValues(self):
        pass
           
    
            
class AnalyticalSolutionMask(SolutionMask):
    def __init__(self, case, axisName, fieldName, caseName, setFieldToXAxis=True):
        SolutionMask.__init__(self, case, axisName, fieldName, caseName, setFieldToXAxis=True)
            
    def getFieldValues(self, time):
        if self.fieldName == 'Pressure':
            return self.case.getPressureValuesConstTime(time)
        
    def getCoordinateValues(self):
        return self.case.getPositionValues()
            
        
        
class NumericalSolutionMask(SolutionMask):
    def __init__(self, case, axisName, fieldName, caseName, setFieldToXAxis=True):
        SolutionMask.__init__(self, case, axisName, fieldName, caseName, setFieldToXAxis=True)
        
    def getFieldValues(self, time):
        return self.case.getFieldValuesAtTime(self.fieldName, time)
        
    def getCoordinateValues(self):
        if self.axisName == 'X':
            return self.case.getCoordinateX()
        elif self.axisName == 'Y':
            return self.case.getCoordinateY()
        elif self.axisName == 'Z':
            return self.case.getCoordinateZ()
        else:
            print("Invalid axisName. Only X, Y or Z are allowed.")
            

class PlotSlider(object):
    def __init__(self, maskList, analyticSolution, timeList):
        self.maskList = maskList
        self.timeList = timeList
        
        self.__initialize()
        
        
    def __initialize(self):
        self.__fig, self.__ax = plt.subplots( 1, 1, figsize=(8,8) )
        plt.subplots_adjust(left=0.08, right=0.97, bottom=0.25)
        
        p_a = np.array(terza.getPressureValuesConstTime( g.time[1], 400, z_a ))
    
        

    
    def __isMiddle( vMin, vMax, v ):
        if vMin <= v <= vMax:   return True
        else:                   return False
    
    def __findCloser( value, lista ):
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







if __name__ == '__main__':
    from AnalyticalSolutions import Terzaghi
    from PhysicalPropertyTools.PropertyParser import Properties
    from CGNSTools.CGNSReader import ReadCGNSFile, getTol
    
    
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
    case2.loadPointsOfInterest(func)
    case2.sortPointsOfInterest(3)
    maskList.append( NumericalSolutionMask(case2, 'Z', 'Pressure', 'Numerical Solution', False) )
    
    
    
    
    
    
    
    