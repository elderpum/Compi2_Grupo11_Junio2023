import re
from Abstracto.instruccion import Instruccion
from Tabla.NodeAST import NodeAST
from Tabla.Arbol import Arbol
from Tabla.Tabla_simbolos import TablaSimbolo
from Tabla.Tipo import Tipos, Nativas
from Tabla.Errores import Error
from Diccionario.Diccionario import D_NATIVA
import math

class Nativa(Instruccion):

    def __init__(self, fila_, columna_, expresion_, Nativa_, valor2_=None):
        super().__init__(Tipos.NUMBER, fila_, columna_)
        self.expresion = expresion_
        self.Nativa = Nativa_
        self.valor2 = valor2_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        inst = None
        if self.valor2 is not None:
            valor = self.valor2.Ejecutar(arbol_, tabla_)
            if isinstance(valor, Error): return valor
            try:
                inst = D_NATIVA[self.Nativa.value+"-"+self.expresion.value+"-"+self.valor2.tipo.value]
            except:
                if self.Nativa == Nativas.TRUNC:
                    return Error('Semantico', 'No es posible realizar fixed de ' + valor, self.fila, self.columna)
        else:
            valor = self.expresion.Ejecutar(arbol_, tabla_)
            if isinstance(valor, Error): return valor
            try:
                inst = D_NATIVA[self.Nativa.value+"-"+self.expresion.tipo.value]
            except:
                if self.Nativa == Nativas.UPPERCASE:
                    return Error('Semantico', 'La función Uppercase unicamente acepta String', self.fila, self.columna)
                elif self.Nativa == Nativas.LOWERCASE:
                    return Error('Semantico', 'La función Lowercase unicamente acepta String', self.fila, self.columna)
                elif self.Nativa == Nativas.TOSTRING:
                    return Error('Semantico', 'No es posible convertir '+valor+" a string", self.fila, self.columna)
                else:
                    return Error('Semantico', 'La función '+self.Nativa.value.lower()+" requiere valores numericos", self.fila, self.columna)
        try:
            if self.Nativa == Nativas.STRING and type(valor) == type([]):
                valor = valor[:]
                for x in range(0,len(valor)):
                    valor[x] = valor[x].getValor()
                self.tipo = inst[1]
                return valor
                
            self.tipo = inst[1]
            return eval(inst[0])
        except:
            return Error('Semantico', 'Error en la función '+self.Nativa.value.lower(), self.fila, self.columna)
                
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('NATIVA')
        if self.valor2 is not None:
            nodo.agregarHijo(self.Nativa.value)
            nodo.agregarHijo('(')
            nodo.agregarHijo(self.expresion.value)
            nodo.agregarHijo(',')
            nodo.agregarHijoNodo(self.valor2.getNodo())
            nodo.agregarHijo(')')
        else:
            nodo.agregarHijo(self.Nativa.value)
            nodo.agregarHijo('(')
            nodo.agregarHijoNodo(self.expresion.getNodo())
            nodo.agregarHijo(')')
        return nodo