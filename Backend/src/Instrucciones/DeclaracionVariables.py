from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Simbolo import Simbolo
from ..Helpers.TiposDatos import Tipos
from datetime import datetime

class DeclaracionVariables(Abstracta):
    def __init__(self,identificador, tipo, valor, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.valor = valor
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
    def traducir(self, arbol, tabla):
        pass