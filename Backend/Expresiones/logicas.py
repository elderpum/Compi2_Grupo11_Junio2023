
from ..Diccionario.Diccionario import D_LOGICA
from ..Abstracto.instruccion import Instruccion
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Tipo import Logicas, Tipos
from ..Tabla.Errores import Error

class Logica(Instruccion):

    def __init__(self, operador_:Logicas, fila_, columna_, op1_, op2_=None):
        super().__init__(Tipos.BOOLEAN, fila_, columna_)
        self.operador = operador_
        self.op1 = op1_
        self.op2 = op2_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        izq = None
        der = None        
        operando = ''        
        if self.op2 is not None:
            izq = self.op1.Ejecutar(arbol_, tabla_)
            if isinstance(izq, Error): return izq
            if self.operador.value == "&&":
                if not izq: return izq
            if self.operador.value == "||":
                if izq: return izq
            der = self.op2.Ejecutar(arbol_, tabla_)
            if isinstance(der, Error): return der
            try:
                operando = D_LOGICA[self.op1.tipo.value+self.operador.value+self.op2.tipo.value]
            except:
                return Error("Semantico", "No se puede operar los tipos "+self.op1.tipo.value+" y "+self.op2.tipo.value+
                             " con el operando logico "+operando, self.fila, self.columna)
            return eval(f'izq {operando} der')
        else:
            izq = self.op1.Ejecutar(arbol_, tabla_)
            if isinstance(izq, Error): return izq
            try:
                operando = D_LOGICA[self.operador.value+self.op1.tipo.value]
            except:
                return Error("Semantico", "No se puede negar el tipo "+self.op1.tipo.value, self.fila, self.columna)

            return eval(f'{operando} izq')

    def getNodo(self) -> NodeAST:
        nodo = NodeAST("LOGICA")
        if not self.op2 is None:
            nodo.addHijo(self.operador.value)
            nodo.addHijoNodo(self.op1.getNodo())
        else:
            nodo.addHijoNodo(self.op1.getNodo())
            nodo.addHijo(self.operador.value)
            nodo.addHijoNodo(self.op2.getNodo())
        return nodo
