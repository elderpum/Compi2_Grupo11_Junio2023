from .continue_ import CONTINUE
from .break_ import BREAK
from .return_ import RETURN
from typing import List
from ..Abstracto.instruccion import Instruccion
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Tipo import  Tipos
from ..Tabla.Errores import Error

class IF(Instruccion):

    def __init__(self, funcion_if_,fila_, columna_, instrucionesElse_=None,instruccionElseIf_ = None):
        super().__init__(Tipos.NOTHING, fila_, columna_)
        self.funcion_if = funcion_if_
        self.InstrucionesElse = instrucionesElse_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        res = self.funcion_if.Ejecutar(arbol_, tabla_)
        if isinstance(res, Error): return res        
        if res:
            return res
        elif self.InstrucionesElse is not None:
            for ins in self.InstrucionesElse:
                res = ins.Ejecutar(arbol_, tabla_)
                if isinstance(res, Error):
                    arbol_.errores.append(res)
                elif isinstance(res, RETURN):                     
                    return res
                elif isinstance(res, CONTINUE):
                    return res
                elif isinstance(res, BREAK):
                    return res
            return True
        
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('If')
        nodo.addHijoNodo(self.funcion_if.getNodo())
        nodo.addHijo("Else")
        nodoInst = NodeAST('INSTRUCIONES')
        for ins in self.InstrucionesElse:
            inst = NodeAST("INSTRUCCION")
            inst.addHijoNodo(ins.getNodo())
            nodoInst.addHijoNodo(inst)
        nodo.addHijoNodo(nodoInst)
        nodo.addHijo(";")
        return nodo