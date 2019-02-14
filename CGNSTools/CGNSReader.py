#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 15:08:02 2018

@author: herminio
"""

import h5py
import numpy as np
import os, subprocess


class ReadCGNSFile(object):
    def __init__(self, fileName, gf_info=True, should_round=8):
        self.fileName = fileName
        self.gf_info = gf_info
        self.should_round = should_round

        subprocess.call(["sh", "-c", "cgnsconvert -h " + fileName], stdout=open(os.devnull, 'wb'))

        self.base = h5py.File(fileName).get('BASE#1')
        self.project = self.base.get('project1')

        self.__buildTimeStepDictionary()


    def getTimeStepName( self, timeInstant ):
        try:
            return self.timeStepDict[timeInstant]
        except:
            pass
            print( timeInstant )
            print( 'Invalid time step.' )

    def getFieldValuesAtTime( self, fieldName, time ):
        timeStepName = self.getTimeStepName(time)
        return self.__getValuesAtIndexes(
                self.project.get(timeStepName).get(fieldName).get(' data').value,
                self.indexes)

    def getCoordinateX(self):
        return self.coords[:,0]

    def getCoordinateY(self):
        return self.coords[:,1]

    def getCoordinateZ(self):
        return self.coords[:,2]


    def loadPointsOfInterest(self, funcCondition=None):
        self.indexes = []
        self.coords = []
        X = self.base.get("project1").get("GridCoordinates").get("CoordinateX").get(' data').value
        Y = self.base.get("project1").get("GridCoordinates").get("CoordinateY").get(' data').value
        Z = self.base.get("project1").get("GridCoordinates").get("CoordinateZ").get(' data').value
        if funcCondition != None:
            for x, y, z, i in zip(X, Y, Z, range(X.size)):
                if funcCondition(x, y, z):
                    self.indexes.append(i)
                    self.coords.append([x, y, z])
            self.coords = np.array(self.coords)
        else:
            self.indexes = range(X.size)
            self.coords = np.array([X, Y, Z]).transpose()

    def sortPointsOfInterest(self, coordinateNumber):
        ''' coordinateNumber = 1 -> x
            coordinateNumber = 2 -> y
            coordinateNumber = 3 -> z '''
        aux = zip(*[self.indexes, self.coords[:,0], self.coords[:,1], self.coords[:,2]])
        aux = sorted(aux, key=lambda x: x[coordinateNumber])
        self.coords = np.zeros((len(aux),3))
        self.indexes = []
        for i in range(len(aux)):
            self.coords[i,:] = np.array([aux[i][1], aux[i][2], aux[i][3]])
            self.indexes.append(aux[i][0])




#pressure = prj.get('TimeStep2').get('Pressure').get(' data').value

#-------------------------------------------------------------------------------------------------

    def __getValuesAtIndexes( self, listOfValues, indexes ):
        aux = []
        for i in indexes:
            aux.append( listOfValues[i] )
        return aux

    def __buildTimeStepDictionary(self):
        self.time = self.base.get("TimeIterativeValues").get("TimeValues").get(" data")[()]
        ct = 0
        self.timeStepDict = {}
        for timeStep in self.project.keys():
            if timeStep.find('Time') != -1:
                self.timeStepDict[round(self.time[ct],self.should_round)] = timeStep
                ct += 1

















class ReadCGNSFile2(object):
    def __init__(self, fileName, gf_info=True, should_round=8):
        self.fileName = fileName
        self.gf_info = gf_info
        self.should_round = should_round

        subprocess.call(["sh", "-c", "cgnsconvert -h " + fileName], stdout=open(os.devnull, 'wb'))

        self.base = h5py.File(fileName).get('BASE')
        self.zone = self.base.get('ZONE')

        self.__buildTimeStepDictionary()


    def getTimeStepName( self, timeInstant ):
        try:
            return self.timeStepDict[timeInstant]
        except KeyError:
            print( timeInstant )
            print( 'Invalid time step.' )

    def getFieldValuesAtTime( self, fieldName, time ):
        timeStepName = self.getTimeStepName(time)
        return self.__getValuesAtIndexes(self.zone.get(timeStepName).get(fieldName).get(' data')[()], self.indexes)

    def getCoordinateX(self):
        return self.coords[:,0]

    def getCoordinateY(self):
        return self.coords[:,1]

    def getCoordinateZ(self):
        return self.coords[:,2]


    def loadPointsOfInterest(self, funcCondition=None):
        self.indexes = []
        self.coords = []
        X = self.zone.get("GridCoordinates").get("CoordinateX").get(" data")[()]
        Y = self.zone.get("GridCoordinates").get("CoordinateY").get(" data")[()]
        Z = self.zone.get("GridCoordinates").get("CoordinateZ").get(" data")[()]
        if funcCondition != None:
            for x, y, z, i in zip(X, Y, Z, range(X.size)):
                if funcCondition(x, y, z):
                    self.indexes.append(i)
                    self.coords.append([x, y, z])
            self.coords = np.array(self.coords)
        else:
            self.indexes = range(X.size)
            self.coords = np.array([X, Y, Z]).transpose()

    def sortPointsOfInterest(self, coordinateNumber):
        ''' coordinateNumber = 1 -> x
            coordinateNumber = 2 -> y
            coordinateNumber = 3 -> z '''
        aux = zip(*[self.indexes, self.coords[:,0], self.coords[:,1], self.coords[:,2]])
        aux = sorted(aux, key=lambda x: x[coordinateNumber])
        self.coords = np.zeros((len(aux),3))
        self.indexes = []
        for i in range(len(aux)):
            self.coords[i,:] = np.array([aux[i][1], aux[i][2], aux[i][3]])
            self.indexes.append(aux[i][0])




#pressure = prj.get('TimeStep2').get('Pressure').get(' data').value

#-------------------------------------------------------------------------------------------------

    def __getValuesAtIndexes( self, listOfValues, indexes ):
        aux = []
        for i in indexes:
            aux.append( listOfValues[i] )
        return aux

    def __buildTimeStepDictionary(self):
        self.time = self.base.get("TimeIterativeValues").get("TimeValues").get(" data")[()]
        ct = 0
        self.timeStepDict = {}
        for timeStep in self.zone.keys():
            if timeStep.find('Time') != -1:
                self.timeStepDict[round(self.time[ct],self.should_round)] = timeStep
                ct += 1


def getTol( x, y, tol=1e-5 ):
    if abs(x-y) < tol:  return True
    else:               return False


if __name__ == '__main__':
    import pylab as pl

    g = ReadCGNSFile2( "Results/ResultsTERZA.cgns" )

    def fun(x,y,z):
        if getTol(x, 0) and getTol(y, 0):
            return True
        else:
            return False

    g.loadPointsOfInterest(fun)
    g.sortPointsOfInterest(3)
    p_n = g.getFieldValuesAtTime('Pressure', 400)
    z_n = g.getCoordinateZ()



    pl.plot( p_n, z_n, 'r.-' )
    pl.grid(True)
    pl.show()
