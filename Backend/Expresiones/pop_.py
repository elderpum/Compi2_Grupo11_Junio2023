from ..Expresiones.Variable import Variable
from typing import List
from ..Abstracto.instruccion import Instruccion
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Simbolo import Simbolo
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Tipo import Tipos
from ..Tabla.Errores import Error

class POP(Instruccion):

    def __init__(self, expresion_, fila_, columna_):
        super().__init__(Tipos.ANY, fila_, columna_)
        self.expresion = expresion_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        valor = self.expresion.Ejecutar(arbol_, tabla_)
        if isinstance(valor, Error):return valor
        if self.expresion.tipo == Tipos.ARRAY:
            value = valor.pop()
            if isinstance(value, Simbolo):
                self.tipo = value.getTipo()
                return value.getValor()
            else:
                self.tipo = Tipos.ARRAY
                return value            
        else:
            return Error("Sintactico","Solo se puede ejecutar push en una lista", self.fila, self.columna)
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('POP')
        nodo.addHijo('pop')
        nodo.addHijo('!')
        nodo.addHijo('(')
        nodo.addHijoNodo(self.expresion.getNodo())
        nodo.addHijo(')')
        nodo.addHijo(";")
        return nodo