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
    def __init__(self, ):
        self.foo

    
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
    from CGNSTools.CGNSReader import ReadCGNSFile