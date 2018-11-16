#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 16:28:51 2018

@author: herminio
         Adapted from Ricieri's code.
"""


import numpy as np
import pylab as pl
import math;


# CLASS DEFINITION ==============================================================================

class Mandel( object ):
    def __init__( self, lenght, height, Force, rock, fluid ):
        self.lenght = lenght;
        self.height = height;
        self.F = Force;      
        
        self.mi = fluid.fromMaterialGetProperty( 0, 'Viscosity' );
        self.c_f = fluid.fromMaterialGetProperty( 0, 'Compressibility' );
        
        self.c_s = rock.fromMaterialGetProperty( 0, 'Compressibility' );
        self.permeability = rock.fromMaterialGetProperty( 0, 'Permeability' );
        self.phi = rock.fromMaterialGetProperty( 0, 'Porosity' );
        self.ni = rock.fromMaterialGetProperty( 0, 'PoissonsRatio' )
        self.ni_u = rock.fromMaterialGetProperty( 0, 'UndrainedPoissonsRatio' )
        self.G = rock.fromMaterialGetProperty( 0, 'ShearModulus' );
        self.alpha = rock.fromMaterialGetProperty( 0, 'BiotCoefficient' );
        
        self._calculate_K_s();
        self._calculate_K_f();
        self._calculate_K_phi();
        self._calculate_K();

        self._calculate_H();
        self._calculate_R();
##        self._calculate_alpha();
        self._calculate_K_p();
        self._calculate_B();
        self._calculate_K_u();
##        self._calculate_ni();
        self._calculate_ni_u();
        self._calculate_K_ni_u();
        self._calculate_gama();
        self._calculate_c();
                

    # Internal functions --------------------------------------------------------------------

    def _calculate_K_s( self ):
        if self.c_s == 0.0:
            self.K_s = 1.0e+100
        else:
            self.K_s = 1.0 / self.c_s;

    def _calculate_K_f( self ):
        if self.c_f == 0.0:
            self.K_f = 1.0e+100
        else:
            self.K_f = 1.0 / self.c_f;

    def _calculate_K_phi( self ):
        self.K_phi = self.K_s
            
    def _calculate_K( self ):
        self.K = 2*self.G*( 1 + self.ni ) / ( 3 - 6*self.ni )
        
    def _calculate_H( self ):
        self.H = 1.0 / ( ( 1.0 / self.K ) - ( 1.0 / self.K_s ) );

    def _calculate_R( self ):
        self.R = 1.0 / ( ( 1.0 / self.H ) + self.phi * ( ( 1.0 / self.K_f ) - ( 1.0 / self.K_phi ) ) );

    def _calculate_alpha( self ):
        self.alpha = 1.0 - ( self.K / self.K_s );

    def _calculate_K_p( self ):
        self.K_p = self.phi * self.K / self.alpha;

    def _calculate_B( self ):
        self.B = self.R / self.H;

    def _calculate_K_u( self ):
        self.K_u = self.K / ( 1.0 - self.alpha * self.B );

    def _calculate_ni( self ):
        self.ni = ( 3.0 * self.K - 2.0 * self.G ) / ( 2.0 * ( 3.0 * self.K + self.G ) );

    def _calculate_ni_u( self ):
        self.ni_u = ( ( 3.0 * self.ni + self.alpha * self.B * ( 1.0 - 2.0 * self.ni ) ) /
                          ( 3.0 - self.alpha * self.B * ( 1.0 - 2.0 * self.ni ) ) );

    def _calculate_K_ni_u( self ):
        self.K_ni_u = ( 3.0 * self.K_u * ( 1.0 - self.ni_u ) ) / ( 1.0 + self.ni_u );

    def _calculate_c_s( self ):
        self.c_s = 1.0 / self.K_s;

    def _calculate_c_f( self ):
        self.c_f = 1.0 / self.K_f;

    def _calculate_gama( self ):
        self.gama = ( self.B * ( 1.0 + self.ni_u ) ) / ( 3.0 * ( 1.0 - self.ni_u ) );

    def _calculate_c( self ):
        self.c = ( ( 2.0 * self.permeability * self.G * ( 1.0 - self.ni ) * ( self.ni_u - self.ni ) ) /
                   ( self.mi * ( self.alpha ** 2.0 ) * ( 1.0 - self.ni_u ) * ( ( 1.0 - 2.0 * self.ni ) ** 2.0 ) ) );


    def _calculateFunctionToFindTheRoots( self, x ):
            y = math.tan( x ) - ( ( 1 - self.ni ) / ( self.ni_u - self.ni ) ) * x;
            return y;


    def _calculateRoots( self, numberOfRoots, maxIterations = 100, maxResidue = 1.0e-12 ):
        roots = [ ];
        for i in range( 0, numberOfRoots ):
            x_A = i * math.pi + maxResidue;
            x_B = i * math.pi + ( math.pi / 2 ) - maxResidue;
            x_C = ( x_A + x_B ) / 2;
            y_C = self._calculateFunctionToFindTheRoots( x_C );
            iteration = 0;
            residue = 1.0;
            while iteration < maxIterations and residue > maxResidue and y_C != 0:
                y_A = self._calculateFunctionToFindTheRoots( x_A );
                y_C = self._calculateFunctionToFindTheRoots( x_C );
                if y_A * y_C > 0.0:
                        x_A = x_C;
                else:
                        x_B = x_C;
                x_C = ( x_A + x_B ) / 2;                
                residue = x_B - x_A;
                iteration += 1;
            roots.append( x_C );
        return roots;


    def __getPositionValuesAndSize( self, ny, funcPosition ):
        if type( ny ) == int:
            positionValues = funcPosition( ny );
            size = ny
        elif type( ny ) == np.ndarray:
            positionValues = ny
            size = ny.size
        elif type( ny ) == list:
            positionValues = ny
            size = len( ny )
        return positionValues, size




    # Class interface -----------------------------------------------------------------------
    def getXPositionValues( self, nx = 200 ):
        dx = self.lenght / ( nx - 1.0 );
        positionValues = [ ];
        for i in range( 0, nx ):
            positionValues.append( i * dx );        
        return positionValues;


    def getXPositionValuesNormalized( self, nx = 200 ):
        positionValues = self.getXPositionValues( nx );
        positionValuesNormalized = [ ];
        for i in range( 0, len( positionValues ) ):
            positionValuesNormalized.append( positionValues[ i ] / self.lenght );
        return positionValuesNormalized;


    def getYPositionValues( self, ny = 200 ):
        dy = self.height / ( ny - 1 );
        positionValues = [ ];
        for i in range( 0, ny ):
            positionValues.append( i * dy );
        return positionValues;


    def getYPositionValuesNormalized( self, ny = 200 ):
        positionValues = self.getYPositionValues( ny );
        positionValuesNormalized = [ ];
        for i in range( 0, len( positionValues ) ):
            positionValuesNormalized.append( positionValues[ i ] / self.height );
        return positionValuesNormalized;


    def getPressureValue( self, xPosition, time, numberOfSummationTerms = 200, roots = [ ] ):
        if time == 0.0:
            pressureValue = self.F * self.B * ( 1 + self.ni_u ) / ( self.lenght * 3 )
            return pressureValue
        else:
            if len( roots ) == 0:
                roots = self._calculateRoots( numberOfSummationTerms )
            summationResult = 0.0
            for i in range( 0, numberOfSummationTerms ):
                term_1 = math.sin( roots[ i ] ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) )
                term_2 = math.cos( roots[ i ] * xPosition / self.lenght ) - math.cos( roots[ i ] )
                term_3 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) )
                summationResult += term_1 * term_2 * term_3
            pressureValue = ( ( 2 * self.F * self.B * ( 1 + self.ni_u ) ) / ( 3 * self.lenght ) ) * summationResult
            return pressureValue


    def getVertStressValue( self, xPosition, time, numberOfSummationTerms = 200, roots = [ ] ):
        if time == 0.0:
            vertStressValue = - self.F / self.lenght
            return vertStressValue
        else:                
            if len( roots ) == 0:
                    roots = self._calculateRoots( numberOfSummationTerms )            
            summationResult_1 = 0.0
            summationResult_2 = 0.0
            for i in range( 0, numberOfSummationTerms ):
                term_1 = math.sin( roots[ i ] ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) )
                term_2 = math.cos( roots[ i ] * xPosition / self.lenght )
                term_3 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) )
                summationResult_1 += term_1 * term_2 * term_3
            for i in range( 0, numberOfSummationTerms ):
                term_1 = ( math.sin( roots[ i ] ) * math.cos( roots[ i ] ) ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) )
                term_2 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) )
                summationResult_2 += term_1 * term_2
            vertStressValue = ( - ( 2 * self.F * ( self.ni_u - self.ni ) ) / ( self.lenght * ( 1 - self.ni ) ) * summationResult_1 -
                          self.F / self.lenght +
                          2 * self.F / self.lenght * summationResult_2 )
            return vertStressValue


    def getHorDisplacementValue( self, xPosition, time, numberOfSummationTerms = 200, roots = [ ] ):
        if len( roots ) == 0:
            roots = self._calculateRoots( numberOfSummationTerms );
        summationResult_1 = 0.0;
        summationResult_2 = 0.0;
        for i in range( 0, numberOfSummationTerms ):
            term_1 = ( math.sin( roots[ i ] ) * math.cos( roots[ i ] ) ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
            term_2 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
            summationResult_1 += term_1 * term_2;
        for i in range( 0, numberOfSummationTerms ):
            term_1 = math.cos( roots[ i ] ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
            term_2 = math.sin( roots[ i ] * xPosition / self.lenght );
            term_3 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
            summationResult_2 += term_1 * term_2 * term_3;
        firstTerm = ( ( self.F * self.ni ) / ( 2 * self.G * self.lenght ) - ( self.F * self.ni_u ) / ( self.G * self.lenght ) * summationResult_1 ) * xPosition;
        secondTerm = self.F / self.G * summationResult_2;
        horDisplacementValue = firstTerm + secondTerm;
        return horDisplacementValue;


    def getVertDisplacementValue( self, yPosition, time, numberOfSummationTerms = 200, roots = [ ] ):
        if len( roots ) == 0:
            roots = self._calculateRoots( numberOfSummationTerms );
        summationResult = 0.0;
        for i in range( 0, numberOfSummationTerms ):
            term_1 = ( math.sin( roots[ i ] ) * math.cos( roots[ i ] ) ) / ( roots[ i ] - math.sin( roots[ i ] ) * math.cos( roots[ i ] ) );
            term_2 = math.exp( - ( ( self.c * time * ( roots[ i ] ** 2 ) ) / ( self.lenght ** 2 ) ) );
            summationResult += term_1 * term_2;
        vertDisplacementValue = ( ( self.F * ( 1.0 - self.ni_u ) ) / ( self.G * self.lenght ) * summationResult -
                                  ( self.F * ( 1.0 - self.ni ) ) / ( 2.0 * self.G * self.lenght ) ) * yPosition;
        return vertDisplacementValue;


    def getPressureValuesConstTime( self, time, nx = 200, numberOfSummationTerms = 200 ):
        '''If nx is an interger, then a list of equally spaced vertical position will be created. However, nx can be
            a list or an numpy array with specified vertical positions.'''
        positionValues, size = self.__getPositionValuesAndSize( nx, self.getXPositionValues )
        roots = self._calculateRoots( numberOfSummationTerms );
        pressureValues = [ ];
        for i in range( 0, size ):
            pressureValue = self.getPressureValue( positionValues[ i ], time, numberOfSummationTerms, roots );
            pressureValues.append( pressureValue );
        return pressureValues;


    def getPressureValuesNormalizedConstTime( self, time, nx = 200, numberOfSummationTerms = 200 ):
        initialPressure = self.getPressureValue( 0.0, 0.0, numberOfSummationTerms );
        pressureValues = self.getPressureValuesConstTime( time, numberOfSummationTerms, nx );
        pressureValuesNormalized = [ ];
        for i in range( 0, len( pressureValues ) ):
            pressureValuesNormalized.append( pressureValues[ i ] / initialPressure );
        return pressureValuesNormalized;


    def getVertStressValuesConstTime( self, time, nx = 200, numberOfSummationTerms = 200 ):
        positionValues, size = self.__getPositionValuesAndSize( nx, self.getXPositionValues )
        roots = self._calculateRoots( numberOfSummationTerms );
        vertStressValues = [ ];
        for i in range( 0, size ):
            vertStressValue = self.getVertStressValue( positionValues[ i ], time, numberOfSummationTerms, roots );
            vertStressValues.append( vertStressValue );
        return vertStressValues;


    def getVertStressValuesNormalizedConstTime( self, time, nx = 200, numberOfSummationTerms = 200 ):
        initialVertStress = self.getVertStressValue( 0.0, 0.0, numberOfSummationTerms )
        vertStressValues = self.getVertStressValuesConstTime( time, numberOfSummationTerms, nx )
        vertStressValuesNormalized = []
        for i in range( 0, len( vertStressValues ) ):
            vertStressValuesNormalized.append( vertStressValues[ i ] / initialVertStress )
        return vertStressValuesNormalized


    def getHorDisplacementValuesConstTime( self, time, nx = 200, numberOfSummationTerms = 200 ):
        positionValues, size = self.__getPositionValuesAndSize( nx, self.getXPositionValues )
        roots = self._calculateRoots( numberOfSummationTerms );
        horDisplacementValues = [ ];
        for i in range( 0, size ):
            horDisplacementValue = self.getHorDisplacementValue( positionValues[ i ], time, numberOfSummationTerms, roots );
            horDisplacementValues.append( horDisplacementValue );

        return horDisplacementValues;


    def getVertDisplacementValuesConstTime( self, time, ny = 200, numberOfSummationTerms = 200 ):
        positionValues, size = self.__getPositionValuesAndSize( ny, self.getYPositionValues )
        roots = self._calculateRoots( numberOfSummationTerms );
        vertDisplacementValues = [ ];
        for i in range( 0, size ):
            vertDisplacementValue = self.getVertDisplacementValue( positionValues[ i ], time, numberOfSummationTerms, roots );
            vertDisplacementValues.append( vertDisplacementValue );
        return vertDisplacementValues;


    def getTimeValues( self, totalTimeInterval, timePoints = 200 ):
        timeValues = np.linspace(0, totalTimeInterval, timePoints )
        return timeValues;                


    def getPressureValuesConstPosition( self, xPosition, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
        timeValues = self.getTimeValues( totalTimeInterval, timePoints );
        roots = self._calculateRoots( numberOfSummationTerms );
        pressureValues = [ ];
        for i in range( 0, len( timeValues ) ):
            pressureValue = self.getPressureValue( xPosition, timeValues[ i ], numberOfSummationTerms, roots );
            pressureValues.append( pressureValue );
        return pressureValues;


    def getPressureValuesNormalizedConstPosition( self, xPosition, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
        initialPressure = self.getPressureValue( 0.0, 0.0, numberOfSummationTerms );
        pressureValues = self.getPressureValuesConstPosition( xPosition, totalTimeInterval, numberOfSummationTerms, timePoints );
        pressureValuesNormalized = [ ];
        for i in range( 0, len( pressureValues ) ):
            pressureValuesNormalized.append( pressureValues[ i ] / initialPressure );
        return pressureValuesNormalized;

    
    def getVertStressValuesConstPosition( self, xPosition, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
        timeValues = self.getTimeValues( totalTimeInterval, timePoints );
        roots = self._calculateRoots( numberOfSummationTerms );
        vertStressValues = [ ];
        for i in range( 0, len( timeValues ) ):
            vertStressValue = self.getVertStressValue( xPosition, timeValues[ i ], numberOfSummationTerms, roots );
            vertStressValues.append( vertStressValue );
        return vertStressValues;


    def getHorDisplacementValuesConstPosition( self, xPosition, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
        timeValues = self.getTimeValues( totalTimeInterval, timePoints );
        roots = self._calculateRoots( numberOfSummationTerms );
        horDisplacementValues = [ ];
        for i in range( 0, len( timeValues ) ):
            horDisplacementValue = self.getHorDisplacementValue( xPosition, timeValues[ i ], numberOfSummationTerms, roots );
            horDisplacementValues.append( horDisplacementValue );
        return horDisplacementValues;


    def getVertDisplacementValuesConstPosition( self, yPosition, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
        timeValues = self.getTimeValues( totalTimeInterval, timePoints );
        roots = self._calculateRoots( numberOfSummationTerms );
        vertDisplacementValues = [ ];
        for i in range( 0, len( timeValues ) ):
            vertDisplacementValue = self.getVertDisplacementValue( yPosition, timeValues[ i ], numberOfSummationTerms, roots );
            vertDisplacementValues.append( vertDisplacementValue );
        return vertDisplacementValues;        
        



if __name__ == '__main__':
    import pylab as pl
    import sys, os
    os.chdir("..")
    current_dir = os.getcwd()
    sys.path.append(current_dir+'/PhysicalPropertyTools')
    from PropertyParser import Properties
    
    lenght = 5.0
    height = 1.0
    Force = 5.0e+7
    rock = Properties( current_dir + "/PhysicalPropertyTools/Json_Files/solid.json" )
    fluid = Properties( current_dir + "/PhysicalPropertyTools/Json_Files/fluid.json" )
    
    mandel = Mandel( lenght, height, Force, rock, fluid )
    AxisX = mandel.getXPositionValues();
    AxisY = mandel.getYPositionValues();
    AxisXNormalized = mandel.getXPositionValuesNormalized();
    AxisYNormalized = mandel.getYPositionValuesNormalized();




    
