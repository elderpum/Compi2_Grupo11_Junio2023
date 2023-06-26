from Tabla.Nodo_list import Node_list
from Tabla.Simbolo import Simbolo
from Expresiones.Variable import Variable
from Abstracto.instruccion import Instruccion
from Tabla.NodeAST import NodeAST
from Tabla.Arbol import Arbol
from Tabla.Tabla_simbolos import TablaSimbolo
from Tabla.Tipo import CICLICO, Tipos
from Tabla.Errores import Error

class FUNCION(Instruccion):

    def __init__(self, id_, instruciones_,fila_, columna_, parametros_=[]):
        super().__init__(Tipos.FUNCTION, fila_, columna_)
        self.id = id_
        self.parametros = parametros_
        self.instruciones = instruciones_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        variable = tabla_.getvariable(self.id)
        if variable == None:
            nombre = self.id+"("
            para = False
            for par in self.parametros:
                nombre+=par[0]+","
                para = True
            if para:
                nombre = nombre[0:len(nombre)-1]
            nombre+=")"
            arbol_.Lista_Simbolo.Agregar(Node_list(self.id, nombre, tabla_.Entorno, self.fila, self.columna))
            tabla_.setVariable(Simbolo([self.parametros, self.instruciones, self.id], Tipos.FUNCTION, self.id, self.fila, self.columna))
        else:
            return Error("Sintactico","Ya existe una funcion con este nombre ", self.fila, self.columna)
        
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('FUNCTION')
        nodo.addHijo(self.id)
        nodo.addHijo("(")
        if len(self.parametros):
            para = None
            anterio = None
            for par in self.parametros:
                para = NodeAST("PARAMETROS")
                if anterio is not None:
                    para.addHijoNodo(anterio)
                    para.addHijo(",")
                    
                para.agregarHijo(par[0])
                if par[1] != Tipos.ANY:
                    para.addrHijo("::")
                    para.addHijo(par[1].value)
                anterio = para
            nodo.addHijoNodo(para)
        nodo.addHijo(")")
        inst = NodeAST("INSTRUCCIONES")
        for ins in self.instruciones:
            insts = NodeAST("INSTRUCCION")
            insts.addHijoNodo(ins.getNodo())
            inst.addHijoNodo(insts)
        nodo.addHijoNodo(inst)
        nodo.addHijo(";")
        return nodo