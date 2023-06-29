from ...Abstracta.Abstracta import Abstracta
from ...TablaSimbolos.TablaSimbolos import TablaSimbolos
from ...TablaSimbolos.Error import Error
from ...Helpers.TiposDatos import Tipos
from ...Expresiones.AccesoArray import AccesoArray
from datetime import datetime

class Length(Abstracta):
    def __init__(self,identificador, fila, columna):
        self.identificador = identificador
        self.tipo = Tipos.NUMBER
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        if isinstance(self.identificador,AccesoArray):
            simbolo = tabla.getSimbolo(self.identificador.identificador)
            if simbolo == None: return Error('Sintactico','La variable no esta definida '+str(self.identificador.identificador), self.fila, self.columna,datetime.now().date())
            if isinstance(simbolo.getValor(), str) or isinstance(simbolo.getValor(), list):
                ind = self.identificador.indice[0].interpretar(arbol,tabla)
                if isinstance(ind,Error): return ind
                return len(simbolo.getValor()[ind])
            else: 
                return Error('Semantico', 'El parametro debe ser STRING',self.fila, self.columna, datetime.now().date())
        else:
            simbolo = tabla.getSimbolo(self.identificador)
            if simbolo == None: return Error('Sintactico','La variable no esta definida ', self.fila, self.columna,datetime.now().date())
            if isinstance(simbolo.getValor(), str) or isinstance(simbolo.getValor(), list):
                return len(simbolo.getValor())
            else: 
                return Error('Semantico', 'El parametro debe ser STRING',self.fila, self.columna, datetime.now().date())
        
    def getTipo(self):
        return self.tipo
    def traducir(self, arbol, tabla):
        pass