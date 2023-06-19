from ..Abstracto.instruccion import Instruccion
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Simbolo import Simbolo
from ..Tabla.Tipo import Tipos
from ..Tabla.Errores import Error

class ARRAY(Instruccion):

    def __init__(self, expresion_, fila_, columna_):
        super().__init__(Tipos.ARRAY, fila_, columna_)
        self.expresion = expresion_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        valor = []
        for exp in self.expresion:
            res = exp.Ejecutar(arbol_, tabla_)
            if isinstance(res, Error): return res
            if exp.tipo == Tipos.ARRAY:
                valor.append(res)
            else:
                valor.append(Simbolo(res, exp.tipo, "", self.fila, self.columna))
        return valor
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('ARRAY')
        lista = None
        anterior = None
        nodo.addHijo("[")
        for exp in self.expresion:
            lista = NodeAST('LISTA_ARRAY')
            if anterior is not None:
                lista.addHijoNodo(anterior)
                lista.addHijo(",")
            lista.addHijoNodo(exp.getNodo())
            anterior = lista
        nodo.addHijoNodo(lista)
        nodo.addHijo("]")
        return nodo