from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Traductor import Traductor
from ..Helpers.TiposDatos import Tipos
from ..Helpers.ReturnCo import ReturnCo
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
        genAux = Traductor()
        traductor = genAux.obtenerInstancia()
        
        traductor.nuevoComentario('Acceso a variable')
        simbolo = tabla.getSimbolo3(self.identificador)
        if simbolo == None:
            traductor.nuevoComentario('Error al acceder a la variable')
            return Error('Semantico', 'Variable no encontrada ',self.fila, self.columna, datetime.now().date())
        temporal = traductor.agregarTemporal()
        temporalPos = simbolo.posicion
        
        if not simbolo.isGlobal:
            temporalPos = traductor.agregarTemporal()
            traductor.agregarExpresion(temporalPos,'P',simbolo.posicion,'+')
        traductor.getStack(temporal,temporalPos)
        
        if simbolo.getTipo() == Tipos.BOOLEAN:
            traductor.nuevoComentario('FIN ACCESO A VARIABLE')
            traductor.agregarEspacio()
            return ReturnCo(temporal,simbolo.getTipo(),True)
        
        if self.trueLbl == '':
            self.trueLbl = traductor.nuevaEtiqueta()
        if self.falseLbl == '':
            self.falseLbl = traductor.nuevaEtiqueta()
        traductor.agregarIf(temporal, '1', '==',self.trueLbl)
        traductor.agregarGoto(self.falseLbl)
        traductor.nuevoComentario('FIN ACCESO A VARIABLE')
        traductor.agregarEspacio()
        ret = ReturnCo(None,Tipos.BOOLEAN, True)
        return ret
