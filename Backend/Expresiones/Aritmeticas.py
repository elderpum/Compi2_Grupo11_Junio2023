from ..Abstracto.instruccion import Instruccion
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Tipo import Tipos, Aritmeticos
from ..Tabla.Errores import Error
from ..Diccionario.Diccionario import Dic_Aritmetica
import math
class Aritmetica(Instruccion):

    def __init__(self, operador: Aritmeticos, fila, columna, op1, op2=None):
        super().__init__(Tipos.ENTERO, fila, columna)
        self.operador = operador
        self.op1 = op1
        self.op2 = op2 
        
    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        izq = None
        der = None
        operando = None
        if self.op2 is not None:
            izq = self.op1.Ejecutar(arbol_, tabla_)
            if isinstance(izq, Error): return izq
            der = self.op2.Ejecutar(arbol_, tabla_)
            if isinstance(der, Error): return der
            try:
                tipo = Dic_Aritmetica[self.op1.tipo.value+self.operador.value+self.op2.tipo.value]
                self.tipo = tipo[0]
                operando = tipo[1]
            except:
                return Error("Semantico", "No se puede operar los tipos "+self.op1.tipo.value+" y "+self.op2.tipo.value+
                             " con el operando "+self.operador.value, self.fila, self.columna)
            if operando.value == "^":
                res = math.pow(izq, der)
                if self.tipo == Tipos.ENTERO:
                    return int(res)
                else:
                    return res
            return eval(f'izq {operando.value} der')
        else:
            izq = self.op1.Ejecutar(arbol_, tabla_)
            if isinstance(izq, Error): return izq
            try:
                tipo = Dic_Aritmetica[self.operador.value+self.op1.tipo.value]
                self.tipo = tipo[0]
                operando = tipo[1]
            except:
                return Error("Semantico", "No se puede operar el tipo "+self.op1.tipo.value+
                             " con la operación de negativo", self.fila, self.columna)
            return eval(f'{operando.value} izq')

    def getNodo(self) -> NodeAST:
        nodo = NodeAST("ARITMETICA")
        if  self.op2 is None:
            nodo.agregarHijo(self.operador.value)
            nodo.agregarHijoNodo(self.op1.getNodo())
        else:
            nodo.agregarHijoNodo(self.op1.getNodo())
            nodo.agregarHijo(self.operador.value)
            nodo.agregarHijoNodo(self.op2.getNodo())
        return nodo
