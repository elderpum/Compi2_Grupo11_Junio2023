from ...Abstracta.Abstracta import Abstracta
from ...TablaSimbolos.TablaSimbolos import TablaSimbolos
from ...TablaSimbolos.Error import Error
from ...Helpers.TiposDatos import Tipos
from ...Expresiones.Primitivas import Primitivas
from datetime import datetime

class TypeOf(Abstracta):
    def __init__(self,identificador, fila, columna):
        self.identificador = identificador
        self.tipo = Tipos.STRING
        super().__init__(fila, columna)
    def interpretar(self, arbol, tabla):
        if self.identificador == None: return Error('Sintactico', 'Se necesita parametro', self.fila, self.columna,datetime.now().date())
        identificador = self.identificador.interpretar(arbol, tabla)
        #simbolo = tabla.getSimbolo(self.identificador)
        if identificador == None: return Error('Sintactico','La variable no esta definida', self.fila, self.columna,datetime.now().date()) #agregar array
        return 'number' if self.identificador.getTipo() == Tipos.NUMBER else 'boolean' if self.identificador.getTipo() == Tipos.BOOLEAN else 'string' if self.identificador.getTipo() == Tipos.STRING else 'any'
    def getTipo(self):
        return self.tipo
    def traducir(self, arbol, tabla):
        pass