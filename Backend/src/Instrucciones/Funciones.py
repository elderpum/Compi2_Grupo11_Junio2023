from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.Error import Error
from .ReturnC import Return

class Funciones(Abstracta):
    def __init__(self,identificador, parametros, instrucciones, tipo ,fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.tipo = tipo
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        #entorno = TablaSimbolos(self.identificador,tabla)
        for instruccion in self.instrucciones:
            value = instruccion.interpretar(arbol, tabla)
            if isinstance(value, Error): return value
            if isinstance(value, Return):
                self.tipo = value.tipo
                return value.value
        return None
    def traducir(self, arbol, tabla):
        pass