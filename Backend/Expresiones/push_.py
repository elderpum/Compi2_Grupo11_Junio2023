from ..Expresiones.Variable import Variable
from typing import List
from ..Abstracto.instruccion import Instruccion
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Simbolo import Simbolo
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Tipo import  Tipos
from ..Tabla.Errores import Error

class PUSH(Instruccion):

    def __init__(self, array_, expresion_, fila_, columna_):
        super().__init__(Tipos.ANY, fila_, columna_)
        self.expresion = expresion_
        self.array = array_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        arr = self.array.Ejecutar(arbol_, tabla_)
        if isinstance(arr, Error):return arr
        if self.array.tipo == Tipos.ARRAY:
            value = self.expresion.Ejecutar(arbol_, tabla_)
            if isinstance(arr, Error):return value
            if self.expresion.tipo == Tipos.ARRAY:
                arr.append(value)
            else:
                arr.append(Simbolo(value, self.expresion.tipo, "", self.fila, self.columna))            
        else:
            return Error("Sintactico","Solo se puede ejecutar push en una estructura de tipo ARRAY", self.fila, self.columna)
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('PUSH')
        nodo.addHijo('push')
        nodo.addHijo('!')
        nodo.addHijo('(')
        nodo.addHijoNodo(self.array.getNodo())
        nodo.addHijo(",")
        nodo.addHijoNodo(self.expresion.getNodo())
        nodo.addHijo(')')
        nodo.addHijo(";")
        return nodo