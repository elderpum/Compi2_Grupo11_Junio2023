from ...Abstracta.Abstracta import Abstracta
from ...TablaSimbolos.TablaSimbolos import TablaSimbolos
from ...TablaSimbolos.Error import Error
from ...Helpers.TiposDatos import Tipos
from ...Expresiones.Primitivas import Primitivas
from datetime import datetime

class Split(Abstracta):
    def __init__(self, identificador,separador ,fila, columna):
        self.identificador = identificador
        self.separador = separador
        self.tipo = Tipos.STRING #cambiar a array despues
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getSimbolo(self.identificador)
        if simbolo == None: return Error('Sintactico','La variable no esta definida', self.fila, self.columna,datetime.now().date())
        if isinstance(simbolo.getValor(), str):
            
            if self.separador == None:
                self.separador = Primitivas(Tipos.STRING," ",self.fila, self.columna)
            if self.separador.getTipo() == Tipos.STRING:
                separador = self.separador.interpretar(arbol, tabla)
                if separador == "" :
                    return list(str(simbolo.getValor()))
                return str(simbolo.getValor()).split(separador)
            else:
                return Error('Semantico', 'El sepaarador debe ser STRING',self.fila, self.columna, datetime.now().date())
        else: 
            return Error('Semantico', 'El identificador debe ser STRING',self.fila, self.columna, datetime.now().date())
    def getTipo(self):
        return self.tipo
    def traducir(self, arbol, tabla):
        pass