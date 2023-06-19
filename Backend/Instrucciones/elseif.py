from .continue_ import CONTINUE
from .break_ import BREAK
from .return_ import RETURN
from typing import List
from Abstracto.instruccion import Instruccion
from Tabla.NodeAST import NodeAST
from Tabla.Arbol import Arbol
from Tabla.Tabla_simbolos import TablaSimbolo
from Tabla.Tipo import  Tipos
from Tabla.Errores import Error

class ELSEIF(Instruccion):

    def __init__(self, expresionIf_, instrucionesIf_,fila_, columna_, elseif_=None):
        super().__init__(Tipos.ANY, fila_, columna_)
        self.ExpresionIf = expresionIf_
        self.InstrucionesIf = instrucionesIf_
        self.elseif = elseif_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        
        if self.elseif is not None:
                res = self.elseif.Ejecutar(arbol_, tabla_)
                if isinstance(res, Error): return res
                if res is not False:
                    return res
                
        condicion = self.ExpresionIf.Ejecutar(arbol_, tabla_)
        if isinstance(condicion, Error): return condicion        
        if self.ExpresionIf.tipo == Tipos.BOOLEAN:
            if condicion:
                for ins in self.InstrucionesIf:
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
            return False
        else:
            return Error("Semantico","La condición de la función if debe ser un booleano",self.fila, self.columna)
    
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('IF')
        if self.elseif is None:
            nodo.addHijo("if")
        else:
            nodo.addHijoNodo(self.elseif.getNodo())
            nodo.addHijo("elseif")
        nodo.addHijoNodo(self.ExpresionIf.getNodo())
        
        nodoInst = NodeAST('INSTRUCIONES')
        for ins in self.InstrucionesIf:
            inst = NodeAST("INSTRUCION")
            inst.addHijoNodo(ins.getNodo())
            nodoInst.addHijoNodo(inst)
        nodo.addHijoNodo(nodoInst)
        return nodo
        