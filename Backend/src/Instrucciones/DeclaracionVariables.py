from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Simbolo import Simbolo
from ..TablaSimbolos.Simbolo import SimboloC
from ..Helpers.TiposDatos import Tipos
from ..TablaSimbolos.Traductor import Traductor
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..Helpers.ReturnCo import ReturnCo
from datetime import datetime

class DeclaracionVariables(Abstracta):
    def __init__(self,identificador, tipo, valor, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.valor = valor
        self.find = True
        self.ghost = -1
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        if self.valor == None:
            if self.tipo == Tipos.NUMBER:
                simbolo = Simbolo(str(self.identificador),self.tipo, 0,str(tabla.getNombre()),self.fila, self.columna)
                result = tabla.setSimboloTabla(simbolo)
                arbol.getTablaSimbolosGlobalInterpretada()[self.identificador] = simbolo
                if isinstance(result,Error):return result #manejar error semantico
                return None
            elif self.tipo == Tipos.STRING:
                simbolo = Simbolo(str(self.identificador),self.tipo, "",str(tabla.getNombre()),self.fila, self.columna)
                result = tabla.setSimboloTabla(simbolo)
                arbol.getTablaSimbolosGlobalInterpretada()[self.identificador] = simbolo
                if isinstance(result,Error):return result #manejar error semantico
                return None
            elif self.tipo == Tipos.BOOLEAN:
                simbolo = Simbolo(str(self.identificador),self.tipo, False,str(tabla.getNombre()) ,self.fila, self.columna)
                result = tabla.setSimboloTabla(simbolo)
                arbol.getTablaSimbolosGlobalInterpretada()[self.identificador] = simbolo
                if isinstance(result,Error):return result #manejar error semantico
                return None
            elif self.tipo == Tipos.ANY:
                simbolo = Simbolo(str(self.identificador),self.tipo, "",str(tabla.getNombre()) ,self.fila, self.columna)
                result = tabla.setSimboloTabla(simbolo)
                arbol.getTablaSimbolosGlobalInterpretada()[self.identificador] = simbolo
                if isinstance(result,Error):return result #manejar error semantico
                return None

        else:
            valorI = self.valor.interpretar(arbol,tabla)
            if isinstance(valorI, Error): return valorI #manejar error semantico
            if self.tipo != Tipos.ANY:
                if self.tipo == self.valor.tipo:
                    simbolo = Simbolo(str(self.identificador),self.tipo, valorI,str(tabla.getNombre()),self.fila, self.columna)
                    result = tabla.setSimboloTabla(simbolo)
                    arbol.getTablaSimbolosGlobalInterpretada()[self.identificador] = simbolo
                    if isinstance(result,Error):return result #manejar error semantico
                    return None
                else:
                    result = Error("Semantico",'Tipo de dato no corresponde al valor '+str(self.tipo)+' '+str(self.valor.tipo),self.fila, self.columna,datetime.now().date())
                    return result
            else:
                simbolo = Simbolo(str(self.identificador),self.tipo, valorI,str(tabla.getNombre()),self.fila, self.columna)
                result = tabla.setSimboloTabla(simbolo)
                arbol.getTablaSimbolosGlobalInterpretada()[self.identificador] = simbolo
                if isinstance(result,Error):return result #manejar error semantico
                return None
            
    def getTipo(self):
        return self.tipo
    def traducir(self, arbol, tabla:TablaSimbolos):
        genAux = Traductor()
        traductor = genAux.obtenerInstancia()
        traductor.nuevoComentario('DECLARACION DE VARIABLE')
        if self.valor is None:
            if self.tipo == Tipos.STRING:
                value = ReturnCo('',Tipos.STRING,True)
            elif self.tipo == Tipos.BOOLEAN:
                value = ReturnCo(False,Tipos.BOOLEAN,True)
            elif self.tipo == Tipos.NUMBER:
                value = ReturnCo(0,Tipos.NUMBER,True)
            elif self.tipo == Tipos.ANY:
                value = ReturnCo('',Tipos.ANY,True)
        else:
            value = self.valor.traducir(arbol, tabla)
        if isinstance(value,Error): return value
        if self.tipo == value.getType():
            inHeap = value.getType() == Tipos.STRING
            simbolo = SimboloC(self.identificador,self.tipo,0,True,inHeap)
            tabla.setSimboloTabla3(simbolo)
        else: 
            traductor.nuevoComentario('Tipo de datos erroneo asignado')
            result = Error('Semantico','Tipo de datos erroneo asignado',self.fila,self.columna,datetime.now().date())
            return result
        tempPos = simbolo.posicion
        if not simbolo.isGlobal:
            tempPos = traductor.agregarTemporal()
            traductor.agregarExpresion(tempPos,'P',simbolo.posicion, '+')
        if value.getType() == Tipos.BOOLEAN:
            templbl = traductor.nuevaEtiqueta()
            
            traductor.colocarEtiqueta(value.trueLbl)
            traductor.setStack(tempPos, "1")
            
            traductor.agregarGoto(templbl)
            
            traductor.colocarEtiqueta(value.falseLbl)
            traductor.setStack(tempPos, "0")
            traductor.colocarEtiqueta(templbl)
        else: 
            traductor.setStack(tempPos, value.value)
        traductor.nuevoComentario('FIN DECLARACION VARIABLES')