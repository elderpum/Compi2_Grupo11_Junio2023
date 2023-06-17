
from ..Abstracto.instruccion import Instruccion
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Tipo import CICLICO
from ..Tabla.Errores import Error

class RETURN(Instruccion):

    def __init__(self, fila_, columna_, expresion_=True):
        super().__init__(CICLICO.RETURN, fila_, columna_)
        self.expresion = expresion_
        self.valor = None
        self.tipoA = None
        
    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        if len(arbol_.PilaFunc):
            valor = self.expresion.Ejecutar(arbol_, tabla_)
            self.valor = valor
            self.tipoA = self.expresion.tipo
            return self
        return Error("Sintactico","La funcion RETURN unicamente se puede usar en Funciones", self.fila, self.columna)

        
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('RETURN')
        nodo.addHijo("return")
        if type(self.expresion)!=type(True):
            nodo.addHijoNodo(self.expresion.getNodo())
        nodo.addHijo(";")
        return nodo