from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta
from datetime import datetime

class Identificador(Abstracta):
    def __init__(self,identificador, fila, columna,tipo = None):
        self.identificador = identificador
        self.tipo = tipo
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getSimbolo(self.identificador)
        simb = tabla.getObjeto(self.identificador)
        if simbolo == None and simb == None: 
            return Error('Semantico', 'Variable no existe',self.fila,self.columna,datetime.now().date() )
        if simbolo != None:
            self.tipo = simbolo.getTipo()
            return simbolo.getValor()
        elif simb != None:
            self.tipo = simb.getTipo()
            return simb.getAtributos()
    
    def getTipo(self):
        return self.tipo
    
    def getIdentificador(self):
        return self.identificador
    def traducir(self, arbol, tabla):
        pass
