from ...Abstracta.Abstracta import Abstracta
from ...TablaSimbolos.TablaSimbolos import TablaSimbolos
from ...TablaSimbolos.Error import Error
from ...Helpers.TiposDatos import Tipos
from datetime import datetime

class toFixed(Abstracta):
    def __init__(self,identificador, exponente, fila, columna):
        self.identificador = identificador
        self.exponente = exponente
        self.tipo = Tipos.NUMBER
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getSimbolo(self.identificador)
        if simbolo == None: return Error('Sintactico','La variable no esta definida', self.fila, self.columna,datetime.now().date())
        if isinstance(simbolo.getValor(), int) or isinstance(simbolo.getValor(),float):
            exponente = self.exponente.interpretar(arbol,tabla)
            if isinstance(exponente, Error): return exponente
            if self.exponente.getTipo() == Tipos.NUMBER and self.exponente.getTipo() != Tipos.BOOLEAN:
                return round(simbolo.getValor(), exponente)
            elif self.exponente.getTipo() == Tipos.ANY:
                    if isinstance(exponente,int) or isinstance(exponente,float):
                        return round(simbolo.getValor(), exponente)
                         
        else: 
            return Error('Semantico', 'El parametro debe ser STRING',self.fila, self.columna, datetime.now().date())
            
    def getTipo(self):
        return self.tipo
    def traducir(self, arbol, tabla):
        pass