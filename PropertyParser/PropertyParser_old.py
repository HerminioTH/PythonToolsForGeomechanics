"""
Created on Tue Sep 15 15:09:53 2015

@author: herminio
"""
from pyparsing import Word, alphas, alphanums, dictOf, nestedExpr


class Properties( object ):
    def __init__( self, fileName ):
        self.fileName = fileName
        self.__readFile()
        self.parser = self.__parser
        self.__numberOfMaterials = len(self.__parser)
        self.__materialNames = []
        self.__materialProperties = [ {} for i in range( self.__numberOfMaterials ) ]

        self.__buildMaterialNames()
        self.__buildProperties()

    def __readFile( self ):
        f = open( self.fileName, "r" )
        lines = f.readlines()
        self.__data = ''
        for line in lines:
            self.__data += line
        ident = Word( alphas, alphanums + " " + "_" )
        itemlist = dictOf( ident, nestedExpr( "{","}") )
        self.__parser = itemlist.parseString( self.__data )

    def __buildMaterialNames( self ):
        for material in range( self.__numberOfMaterials ):
            self.__materialNames.append( self.__parser[material][0] )

    def __buildProperties( self ):
        for mat in range( self.__numberOfMaterials ):
            props = self.__parser[mat][1]
            for i in range( 0, len(props)-1, 2 ):
                try:
                    self.__materialProperties[mat][props[i]] = float(props[i+1])
                except:
                    self.__materialProperties[mat][props[i]] = str(props[i+1])

    def setProperty( self, PropertyName, PropertyValue, material=0 ):
        self.__materialProperties[material][PropertyName] = PropertyValue

    def getMaterialProperties( self ):
        return self.__materialProperties
        

    def showAllMaterialData( self ):
        print self.__data

    def getMaterialPropertyNames( self, material=0 ):
        return self.__materialProperties[material].keys()

    def getNumberOfMaterials( self ):
        return self.__numberOfMaterials

    def getMaterialProperty( self, propName, material=0 ):
        if self.__numberOfMaterials == 1:         material = 0
        if material+1 > self.__numberOfMaterials: print 'Wrong material'; return 0
        try:
            return self.__materialProperties[material][propName]
        except:
            print 'Material doesn\'t have a property called ' + propName
            print 'Take a look at self.getMaterialPropertyNames().'
            



if __name__ == '__main__':
    rock = Properties( "..\\workspace\\AppGeomechanics3D\\Rock_Properties.txt" )
    fluid = Properties( "..\\workspace\\AppGeomechanics3D\\Fluid_Properties.txt" )



