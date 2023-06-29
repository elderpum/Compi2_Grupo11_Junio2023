from ...Abstracta.Abstracta import Abstracta
from ...TablaSimbolos.TablaSimbolos import TablaSimbolos
from ...TablaSimbolos.Error import Error
from ...Helpers.TiposDatos import Tipos
from datetime import datetime

class toUpper(Abstracta):
    def __init__(self,identificador, fila, columna):
        self.identificador = identificador
        self.tipo = Tipos.STRING
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getSimbolo(self.identificador)
        if simbolo == None: return Error('Sintactico','La variable no esta definida', self.fila, self.columna,datetime.now().date())
        if isinstance(simbolo.getValor(), str):
            return str(simbolo.getValor()).upper()
        else: 
            return Error('Semantico', 'El parametro debe ser STRING',self.fila, self.columna, datetime.now().date())
    def getTipo(self):
        return self.tipo
    def traducir(self, arbol, tabla):
        pass