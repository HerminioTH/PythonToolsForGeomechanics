#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 13:46:09 2018

@author: herminio
"""
import json


class Properties( object ):
    def __init__( self, fileName ):
        self.fileName = fileName
        self.__readJsonFile()
        self.__getMaterials()
        
        
    def fromMaterialGetProperty(self, mat, prop):
        if type(mat) == int:
            try:    
                mat = self.materials[mat]
            except:
                raise
                
        if self.materials.count(mat) != 0:
            props = [p for p in self.data.get(mat).keys()]
            if props.count(prop) != 0:
                return self.data.get(mat).get(prop).get('value')
            else:
                print('Property %s does not belong to material %s'%(prop, mat))
        else:
            print('Material %s is not specified in file %s'%(mat, self.fileName))
        
    
    
    def __getMaterials(self):
        self.materials = [mat for mat in self.data.keys()]
        
    def __readJsonFile(self):
        f = open(self.fileName, "r")
        self.data = json.load(f)
        
    

  



if __name__ == '__main__':
    
    fileName = "Json_Files/solid.json"
    p = Properties(fileName)
    print(p.data)
        


