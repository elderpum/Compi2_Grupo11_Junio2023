from ..Abstracto.instruccion import Instruccion
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Tipo import Tipos, Relacionales
from ..Tabla.Errores import Error
from ..Diccionario.Diccionario import D_Relacional


class Relacional(Instruccion):

    def __init__(self, operador_: Relacionales, fila_, columna_, op1_, op2_):
        super().__init__(Tipos.BOOLEAN, fila_, columna_)
        self.operador = operador_
        self.op1 = op1_
        self.op2 = op2_
        

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        
        izq = self.op1.Ejecutar(arbol_, tabla_)
        if isinstance(izq, Error): return izq

        der = self.op2.Ejecutar(arbol_, tabla_)
        if isinstance(der, Error): return der
        
        try:
            self.tipo = D_Relacional[self.op1.tipo.value+self.operador.value+self.op2.tipo.value]
        except:
            return Error("Semantico", "No se puede operar los tipos "+self.op1.tipo.value+" y "+self.op2.tipo.value+
                            " con el operando relacional "+self.operador.value, self.fila, self.columna)
        return eval(f'izq {self.operador.value} der')

    def getNodo(self) -> NodeAST:
        nodo = NodeAST("RELACIONAL")
        nodo.addHijoNodo(self.op1.getNodo())
        nodo.addHijo(self.operador.value)
        nodo.addHijoNodo(self.op2.getNodo())
        return nodo

    

