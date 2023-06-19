from Abstracto.instruccion import Instruccion
from Tabla.NodeAST import NodeAST
from Tabla.Arbol import Arbol
from Tabla.Tabla_simbolos import TablaSimbolo
from Tabla.Tipo import CICLICO
from Tabla.Errores import Error

class CONTINUE(Instruccion):

    def __init__(self, fila_, columna_):
        super().__init__(CICLICO.CONTINUE, fila_, columna_)

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        if len(arbol_.PilaCiclo):
            return self
        return Error("Sintactico","La funcion CONTINUE unicamente se puede usar en ciclos", self.fila, self.columna)

        
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('CONTINUE')
        return nodo