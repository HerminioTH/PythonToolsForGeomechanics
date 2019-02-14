"""
Created on Thu Nov 15 14:44:02 2018

@author: herminio
         Adapted from Ricieri's code.
"""
import numpy as np
import pylab as pl
import math


# CLASS DEFINITION ==============================================================================

class Solution( object ):
    def __init__( self, height, tao_0, rock, fluid ):
        self.height = height;
        self.tao_0 = tao_0;
        
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
        self._calculate_K_p();
        self._calculate_B();
        self._calculate_K_u();
        self._calculate_ni_u();
        self._calculate_K_ni_u();        
        self._calculate_gama();
        self._calculate_c();
        
        self._calculate_K_v_u();
        self._calculate_c_m();
        self._calculate_p_0();
        self._calculate_v_0();
            

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

    def _calculate_K_p( self ):
        self.K_p = self.phi * self.K / self.alpha;
        
    def _calculate_B( self ):
        self.B = self.R / self.H;

    def _calculate_K_u( self ):
        if self.alpha * self.B != 1.0:
            self.K_u = self.K / ( 1.0 - self.alpha * self.B );
        else:
            self.K_u = 1.0e+100

    def _calculate_ni_u( self ):
        value = ( ( 3.0 * self.ni + self.alpha * self.B * ( 1.0 - 2.0 * self.ni ) ) /
                  ( 3.0 - self.alpha * self.B * ( 1.0 - 2.0 * self.ni ) ) );
        if self.ni_u != value:
            self.ni_u = value
            print ("Undrained Poisson\'s Ratio mismatch")

    def _calculate_K_ni_u( self ):
        self.K_ni_u = ( 3.0 * self.K_u * ( 1.0 - self.ni_u ) ) / ( 1.0 + self.ni_u );

    def _calculate_gama( self ):
        self.gama = ( self.B * ( 1.0 + self.ni_u ) ) / ( 3.0 * ( 1.0 - self.ni_u ) );

    def _calculate_c( self ):
        self.c = ( ( 2.0 * self.permeability * self.G * ( 1.0 - self.ni ) * ( self.ni_u - self.ni ) ) /
                    ( self.mi * ( self.alpha ** 2.0 ) * ( 1.0 - self.ni_u ) * ( ( 1.0 - 2.0 * self.ni ) ** 2.0 ) ) );

    def _calculate_K_v_u( self ):
        self.K_v_u = 3*self.K_u*( 1 - self.ni_u ) / ( 1 + self.ni_u )

    def _calculate_c_m( self ):
        self.c_m = ( self.alpha * ( 1.0 + self.ni ) ) / ( 3.0 * self.K * ( 1.0 - self.ni ) );




    def _calculate_ni( self ):
        self.ni = ( 3.0 * self.K - 2.0 * self.G ) / ( 2.0 * ( 3.0 * self.K + self.G ) );

    def _calculate_alpha( self ):
        self.alpha = 1.0 - ( self.K / self.K_s );
        

    def _calculate_p_0( self ):
        self.p_0 = self.gama * self.tao_0;

    def _calculate_v_0( self ):
        self.v_0 = -self.height * self.tao_0 / self.K_v_u;




    def getPositionValues(self, n=200, axisName=None):
        return self.getPositionValues(n)


    def getPositionValues( self, ny = 200 ):
        dy = self.height / ( ny - 1.0 );
        positionValues = [];
        for i in range( 0, ny ):
            positionValues.append( i * dy );
        return np.array(positionValues)


    def getPositionValuesNormalized( self, ny = 200 ):
        positionValues = self.getPositionValues( ny );
        positionValuesNormalized = [ ];
        for i in range( 0, len( positionValues ) ):
            positionValuesNormalized.append( positionValues[ i ] / self.height );
        return positionValuesNormalized;

    
    def getPressureValue( self, yPosition, time, numberOfSummationTerms = 200 ):
        position = self.height - yPosition;
        if time == 0.0:
            pressureValue = self.p_0
            return pressureValue
        else:
            summationResult = 0
            for j in range( 0, numberOfSummationTerms ):
                term_1 = 1.0 / ( 2.0 * j + 1.0 )
                term_2 = ( math.exp( - ( ( time * self.c * ( math.pi ** 2.0 ) * ( ( 2.0 * j + 1.0 ) ** 2.0 ) ) /
                                        ( 4.0 * ( self.height ** 2.0 ) ) ) ) )
                term_3 = math.sin( ( math.pi * position * ( 2.0 * j + 1 ) ) / ( 2.0 * self.height ) )
                summationResult += term_1 * term_2 * term_3
            pressureValue = 4.0 * self.gama * self.tao_0 * summationResult / math.pi
            return pressureValue

    def getDisplacementValue( self, yPosition, time, numberOfSummationTerms = 200 ):
        position = self.height - yPosition;
        if time == 0.0:
            displacementValue = - ( self.tao_0 * ( self.height - position ) * ( 1 + self.ni_u ) / ( 3 * self.K_u * ( 1 - self.ni_u ) ) )
            return displacementValue
        else:                
            summationResult = 0;
            initialDisplacementValue = ( ( self.tao_0 * ( 1.0 - 2.0 * self.ni_u ) * ( self.height - position ) ) /
                                         ( 2.0 * self.G * ( 1.0 - self.ni_u ) ) )
            for j in range( 0, numberOfSummationTerms ):
                term_1 = 1.0 / ( ( 2.0 * j + 1.0 ) ** 2 )
                term_2 = ( math.exp( - ( ( self.c * time * ( math.pi ** 2.0 ) * ( ( 2.0 * j + 1.0 ) ** 2.0 ) ) /
                                         ( 4.0 * ( self.height ** 2.0 ) ) ) ) )
                term_3 = math.cos( ( math.pi * position * ( 2.0 * j + 1.0 ) ) / ( 2 * self.height ) )
                summationResult += term_1 * term_2 * term_3
            displacementValue = - ( initialDisplacementValue + self.c_m * self.gama * self.tao_0 *
                                  ( ( self.height - position ) - ( 8.0 * self.height / ( math.pi ** 2.0 ) ) * summationResult ) )
            return displacementValue;

    def __getPositionValuesAndSize( self, ny ):
        if type( ny ) == int:
            positionValues = self.getPositionValues( ny );
            size = ny
        elif type( ny ) == np.ndarray:
            positionValues = ny
            size = ny.size
        elif type( ny ) == list:
            positionValues = ny
            size = len( ny )
        return positionValues, size

    def getPressureValuesConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ):
        '''If ny is an interger, then a list of equally spaced vertical position will be created. However, ny can be
            a list or an numpy array with specified vertical positions.'''
        positionValues, size = self.__getPositionValuesAndSize( ny )
        pressureValues = [ ];
        for i in range( 0, size ):
            pressureValue = self.getPressureValue( positionValues[ i ], time, numberOfSummationTerms );
            pressureValues.append( pressureValue );
        return np.array(pressureValues)

    def getPressureValuesNormalizedConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ): # p / p_0
        pressureValues = self.getPressureValuesConstTime( time, numberOfSummationTerms, ny );
        pressureValuesNormalized = [ ];
        for i in range( 0, len( pressureValues ) ):
            pressureValuesNormalized.append( pressureValues[ i ] / self.p_0 );
        return pressureValuesNormalized;

    def getDisplacementValuesConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ):
        '''If ny is an interger, then a list of equally spaced vertical position will be created. However, ny can be
            a list or an numpy array with specified vertical positions.'''
        positionValues, size = self.__getPositionValuesAndSize( ny )
        displacementValues = [ ];
        for i in range( 0, size ):
            displacementValue = self.getDisplacementValue( positionValues[ i ], time, numberOfSummationTerms );
            displacementValues.append( displacementValue );
        return displacementValues;

    def getDisplacementValuesNormalizedConstTime( self, time, numberOfSummationTerms = 200, ny = 200 ): # ( v - v_inicial ) / ( v_final - v_inicial )
        positionValues = self.getPositionValues( ny );
        displacementValues = self.getDisplacementValuesConstTime( time, numberOfSummationTerms, ny );
        displacementValuesNormalized = [ ];
        for i in range( 0, len( displacementValues ) ):
            position = self.height - positionValues[ i ];
            initialDisplacementValue = ( ( self.tao_0 * ( 1.0 - 2.0 * self.ni_u ) * ( self.height - position ) ) /
                                         ( 2.0 * self.G * ( 1.0 - self.ni_u ) ) );
            finalDisplacementValue = initialDisplacementValue + self.c_m * self.gama * self.tao_0 * ( self.height - position );
            if i == 0:
                displacementValueNormalized = 0;
            else:
                displacementValueNormalized = ( ( - displacementValues[ i ] - initialDisplacementValue ) /
                                                ( finalDisplacementValue - initialDisplacementValue ) );
            displacementValuesNormalized.append( displacementValueNormalized );
        displacementValuesNormalized[ 0 ] = displacementValuesNormalized[ 1 ];
        return displacementValuesNormalized;

    def getTimeValues( self, totalTimeInterval, timePoints = 200 ):
        timeValues = np.linspace(0, totalTimeInterval, timePoints )
        return timeValues;

    def getPressureValuesConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
        timeValues = self.getTimeValues( totalTimeInterval, timePoints );
        pressureValues = [ ];
        for i in range( 0, len( timeValues ) ):
            pressureValue = self.getPressureValue( position, timeValues[ i ], numberOfSummationTerms );
            pressureValues.append( pressureValue );
        return pressureValues;


    def getPressureValuesNormalizedConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ): # p / p_0
        pressureValues = self.getPressureValuesConstPosition( position, totalTimeInterval, numberOfSummationTerms, timePoints );
        pressureValuesNormalized = [ ];
        for i in range( 0, len( pressureValues ) ):
            pressureValuesNormalized.append( pressureValues[ i ] / self.p_0 );
        return pressureValuesNormalized;

    def getDisplacementValuesConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ):
        timeValues = self.getTimeValues( totalTimeInterval, timePoints );
        displacementValues = [ ];
        for i in range( 0, len( timeValues ) ):
            displacementValue = self.getDisplacementValue( position, timeValues[ i ], numberOfSummationTerms );
            displacementValues.append( displacementValue );
        return displacementValues;


    def getDisplacementValuesNormalizedConstPosition( self, position, totalTimeInterval, numberOfSummationTerms = 200, timePoints = 200 ): # ( v - v_inicial ) / ( v_final - v_inicial )
        displacementValues = self.getDisplacementValuesConstPosition( position, totalTimeInterval, numberOfSummationTerms, timePoints );
        position = self.height - position;
        initialDisplacementValue = ( ( self.tao_0 * ( 1.0 - 2.0 * self.ni_u ) * ( self.height - position ) ) /
                                     ( 2.0 * self.G * ( 1.0 - self.ni_u ) ) );
        finalDisplacementValue = initialDisplacementValue + self.c_m * self.gama * self.tao_0 * ( self.height - position );
        displacementValuesNormalized = [ ];
        for i in range( 0, len( displacementValues ) ):
            displacementValueNormalized = ( ( - displacementValues[ i ] - initialDisplacementValue ) /
                                            ( finalDisplacementValue - initialDisplacementValue ) );
            displacementValuesNormalized.append( displacementValueNormalized );
        return displacementValuesNormalized;
    





def pEqui( stress, height, c_f, c_s, phi, ni, G, alpha ):
    Lambda = 2*G*ni/(1-2*ni)
    Psi = phi*c_f + ( alpha - phi )*c_s
    Beta = Lambda*(1-ni)/ni + alpha*alpha/Psi
    p = -alpha*stress/( Psi*Beta )
    return p

def uEqui( stress, height, c_f, c_s, phi, ni, G, alpha ):
    Psi = phi*c_f + ( alpha - phi )*c_s
    lame = 2*G*ni/(1-2*ni)
    Beta = lame*(1-ni)/ni + alpha*alpha/Psi
    return stress*height/Beta



if __name__ == '__main__':
    import pylab as pl
    import sys, os
    os.chdir("..")
    current_dir = os.getcwd()
    sys.path.append(current_dir+'/PhysicalPropertyTools')
    from PropertyParser import Properties
    

    height = 6.0
    tao_0 = 1.0e+5
    rock = Properties( current_dir + "/PhysicalPropertyTools/Json_Files/solid.json" )
    fluid = Properties( current_dir + "/PhysicalPropertyTools/Json_Files/fluid.json" )

    terza = Solution( height, tao_0, rock, fluid )
    z_a = terza.getPositionValues()
    p_a = terza.getPressureValuesConstTime(10000, 400)
    
    pl.plot( p_a, z_a, 'b-' )
    pl.grid(True)
    pl.show()






    
