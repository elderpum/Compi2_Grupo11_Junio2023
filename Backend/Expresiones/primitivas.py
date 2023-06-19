from Abstracto.instruccion import Instruccion
from Tabla.NodeAST import NodeAST
from Tabla.Arbol import Arbol
from Tabla.Tabla_simbolos import TablaSimbolo
from Tabla.Tipo import Tipos

class Primitivo(Instruccion):

    def __init__(self, tipo_:Tipos, valor_, fila_, columna_):
        super().__init__(tipo_, fila_, columna_)
        self.valor = valor_

    def getNodo(self) -> NodeAST:
        nodo = NodeAST('PRIMITIVO')
        nodo.addHijo(str(self.valor))
        return nodo

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        return self.valor

