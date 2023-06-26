from Expresiones.Variable import Variable
from typing import List
from Abstracto.instruccion import Instruccion
from Tabla.NodeAST import NodeAST
from Tabla.Nodo_list import Node_list
from Tabla.Arbol import Arbol
from Tabla.Simbolo import Simbolo
from Tabla.Tabla_simbolos import TablaSimbolo
from Tabla.Tipo import Tipos
from Tabla.Errores import Error

class STRUCT(Instruccion):

    def __init__(self, id, parametros,fila, columna, mutable=False):
        super().__init__(Tipos.STRUCT, fila, columna)
        self.id = id
        self.parametros = parametros
        self.mutable = mutable
        
    def Ejecutar(self, arbol: Arbol, tabla: TablaSimbolo):
        variable = tabla.getvariable(self.id)
        content = {1:self.id, 2: self.mutable}
        if variable is None:
            for par in self.parametros:#variable, tipo de variable, tipo obligatorio
                content[par[0]] = [None, None, par[1]]
            arbol.Lista_Simbolo.Agregar(Node_list(self.id, "STRUCT", tabla.Entorno, self.fila, self.columna))
            nuevoSimbolo = Simbolo(content, self.tipo, self.id, self.fila, self.columna)
            tabla.setVariable(nuevoSimbolo)
            return content
        else:
            return Error("Sintactico","No se puede crear un Struct con ese nombre debido que ya hay una variable asignada", self.fila, self.columna)
        
    def getNodo(self) -> NodeAST:
        nodo = NodeAST("STRUCT")
        if self.mutable:
            nodo.addHijo("MUTABLE")
        nodo.addHijo("STRUCT")
        nodo.addHijo(self.id)
        para = None
        anterior = None
        for par in self.parametros:
            para = NodeAST("PARAMETROS")
            tipo = NodeAST("TIPO")
            nid = NodeAST("ID")
            if anterior!=None:
                para.addHijoNodo(anterior)
            nid.addHijo(par[0])
            para.addHijoNodo(nid)
            if par[1] !=None:
                para.addHijo(":")
                para.addHijo(":")
                tipo.addHijo(par[1].value)
                para.addHijoNodo(tipo)
            para.addHijo(";")
            anterior = para
        nodo.addHijoNodo(para)
        nodo.addHijo("end")
        nodo.addHijo(";")    
        return nodo
    
    