from ...Abstracta.Abstracta import Abstracta
from ...TablaSimbolos.TablaSimbolos import TablaSimbolos
from ...TablaSimbolos.Error import Error
from ...Helpers.TiposDatos import Tipos
from ...Expresiones.Identificador import Identificador
from datetime import datetime

class Number(Abstracta):
    def __init__(self,identificador, fila, columna):
        self.identificador = identificador
        self.tipo = Tipos.NUMBER
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        if isinstance(self.identificador,Identificador):
            simbolo = tabla.getSimbolo(self.identificador.identificador)
            if simbolo == None: return Error('Sintactico','La variable no esta definida', self.fila, self.columna,datetime.now().date())
            if not isinstance(simbolo.getValor(), int) or not isinstance(simbolo.getValor(),float):
                return float(simbolo.getValor())
            elif isinstance(simbolo.getValor(),list):
                return Error('Semantico', 'No es posible convertir un ARRAY a NUMBER',self.fila, self.columna, datetime.now().date())
            else: 
                return Error('Semantico', 'El parametro debe ser STRING',self.fila, self.columna, datetime.now().date())
        else: 
            valor = self.identificador.interpretar()
            if isinstance(valor,Error): return valor
            if not isinstance(valor, int) or not isinstance(valor,float):
                return float(valor)
            elif isinstance(valor,list):
                return Error('Semantico', 'No es posible convertir un ARRAY a NUMBER',self.fila, self.columna, datetime.now().date())
            else: 
                return Error('Semantico', 'El parametro debe ser STRING',self.fila, self.columna, datetime.now().date())
        
    def getTipo(self):
        return self.tipo
    def traducir(self, arbol, tabla):
        pass