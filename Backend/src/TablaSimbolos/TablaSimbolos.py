from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.Simbolo import Simbolo
from ..TablaSimbolos.Simbolo import SimboloC
from ..TablaSimbolos.ObjetoStruct import ObjetoStruct
from .DefStruct import DefinicionStruct
from .AtributoS import AtributoStruct
from datetime import datetime

class TablaSimbolos:
    def __init__(self,nombre ,anterior = None):
        self.tabla = {}
        self.tabla3 = {}
        self.nombre = nombre
        self.anterior = anterior
        self.estructuras = []
        self.simbEst = {}
        #####
        self.breakLbl = ''
        self.continueLbl = ''
        self.returnLbl = ''
        self.recTemps = False
        self.size = 0
        if anterior != None:
            self.size = self.anterior.size
        
    def setTabla(self, id, tipo, inHeap, find = True):
        if find:
            actual = self
            while actual != None:
                if id in actual.tabla3:
                    actual.tabla3[id].setTipo(tipo)
                    actual.tabla3[id].setInHeap(inHeap)
                    return actual.tabla3[id]
                else:
                    actual = actual.anterior
        if id in self.tabla3:
            self.tabla3[id].setTipo(tipo)
            self.tabla3[id].setInHeap(inHeap)
            return self.tabla3[id]
        else:
            simbolo = SimboloC(id,tipo,self.size,self.anterior, inHeap)
            self.size+=1
            self.tabla3[id] = simbolo
            return self.tabla3[id]
        
        
    def getSimbEst(self):    
        return self.simbEst
    def actualizarObjeto(self, simbolo):
        actual = self
        while actual != None:
            if simbolo.getIdentificador() in actual.simbEst: 
                actual.simbEst[simbolo.getIdentificador()]= simbolo
                return None
                # validar si se debe cambiar el tipo 
                # actual.tabla[simbolo.getIdentificador()].setTipo(simbolo.getTipo())
            else: 
                actual = actual.anterior
        #agregar a tabla de errores el error
        return Error("Semantico", "La variable no existe, no es posible actualizar", simbolo.getFila(), simbolo.getColumna(),datetime.now().date())
    
    def getObjeto(self, identificador):
        actual = self
        while actual != None:
            if identificador in actual.simbEst:
                return actual.simbEst[identificador]
            else:
                actual = actual.anterior
        return None
    
    def nuevoObjeto(self,estructura):
        if estructura.getIdentificador() in self.simbEst:
            return Error('Semantico', 'Objeto ya existe', estructura.getFila(), estructura.getColumna(), datetime.now().date())
        self.simbEst[estructura.getIdentificador()]= estructura
    
    def getEstructuras(self):
        return self.estructuras
    def nuevaEstructura(self,estructura: DefinicionStruct):
        for estructuraa in self.estructuras:
            if estructura.getIdentificador() == estructuraa.getIdentificador():
                return Error('Semantico', 'Estructura previamente definida', estructura.getFila(), estructura.getColumna(), datetime.now().date())
        self.estructuras.append(estructura)
        return None
    def obtenerEstructura(self, identificador):
        actual = self
        while actual != None:
            for estructura in actual.estructuras:
                if estructura.getIdentificador() == identificador:
                    return estructura
            actual = actual.anterior
        return None
    def getTabla(self):
        return self.tabla
    def getTabla3(self):
        return self.tabla3
    
    def getNombre(self):
        return self.nombre
    
    def setNombre(self, nombre):
        self.nombre = nombre
    
    def getEntorno(self, nombre):
        actual = self
        while actual != None:
            nombrea = str(actual.nombre)
            nombren = str(nombre)
            if nombren in nombrea:
                return actual
            else:
                actual = actual.anterior
        return None
    
    def setSimboloTabla(self, simbolo):
        if simbolo.getIdentificador() in self.tabla:
            return Error('Semantico', 'La variable ya ha sido definida', simbolo.getFila(), simbolo.getColumna(), datetime.now().date())
        else:
            self.tabla[simbolo.getIdentificador()] =simbolo
            return None
    
    def setSimboloTabla3(self, simbolo):
        if simbolo.identificador in self.tabla3:
            return Error('Semantico', 'La variable ya ha sido definida', simbolo.getFila(), simbolo.getColumna(), datetime.now().date())
        else:
            self.tabla3[simbolo.identificador] =simbolo
            return None
    
    def setFuncion(self, simbolo):
        
        if isinstance(simbolo,Simbolo):
            if simbolo.getIdentificador() in self.tabla:
        #manejar el error de variable ya existente
                pass
            else:
                self.tabla[simbolo.getIdentificador()] =simbolo
        elif isinstance(simbolo,ObjetoStruct):
            if simbolo.getIdentificador() in self.simbEst:
        #manejar el error de variable ya existente
                pass
            else:
                self.simbEst[simbolo.getIdentificador()] =simbolo
            
    def getSimbolo(self, identificador):
        actual = self
        while actual != None:
            if identificador in actual.tabla:
                return actual.tabla[identificador]
            else:
                actual = actual.anterior
        return None
    def getSimbolo3(self, identificador):
        actual = self
        while actual != None:
            if identificador in actual.tabla3:
                return actual.tabla3[identificador]
            else:
                actual = actual.anterior
        return None
    
    def actualizarSimbolo(self, simbolo):
        actual = self
        while actual != None:
            if simbolo.getIdentificador() in actual.tabla: 
                actual.tabla[simbolo.getIdentificador()].setValor(simbolo.getValor())
                return None
                # validar si se debe cambiar el tipo 
                # actual.tabla[simbolo.getIdentificador()].setTipo(simbolo.getTipo())
            else: 
                actual = actual.anterior
        #agregar a tabla de errores el error
        return Error("Semantico", "La variable no existe, no es posible actualizar", simbolo.getFila(), simbolo.getColumna(),datetime.now().date())
    
    def actualizarSimbolo3(self, simbolo):
        actual = self
        while actual != None:
            if simbolo.getIdentificador() in actual.tabla3: 
                actual.tabla[simbolo.getIdentificador()].setValor(simbolo.getValor())
                return None
                # validar si se debe cambiar el tipo 
                # actual.tabla[simbolo.getIdentificador()].setTipo(simbolo.getTipo())
            else: 
                actual = actual.anterior
        #agregar a tabla de errores el error
        return Error("Semantico", "La variable no existe, no es posible actualizar", simbolo.getFila(), simbolo.getColumna(),datetime.now().date())
