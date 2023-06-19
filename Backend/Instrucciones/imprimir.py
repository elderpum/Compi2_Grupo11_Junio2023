from typing import List
from Abstracto.instruccion import Instruccion
from Tabla.NodeAST import NodeAST
from Tabla.Arbol import Arbol
from Tabla.Tabla_simbolos import TablaSimbolo
from Tabla.Tipo import Tipos
from Tabla.Errores import Error
from Tabla.Simbolo import Simbolo

class Imprimir(Instruccion):

    def __init__(self, expresion_: List, fila_, columna_):
        super().__init__(Tipos.STRING, fila_, columna_)
        self.expresion = expresion_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        valor = ''
        tamaño = 1
        for ex in self.expresion:
            val = ex.Ejecutar(arbol_, tabla_)
            if isinstance(val, Error): return val
            if ex.tipo == Tipos.OBJECT:
                val = self.getStruct("", val)
            elif ex.tipo == Tipos.STRUCT:
                val = val[1]
            elif ex.tipo == Tipos.ARRAY :
                val = self.getArrayValue(val, "")
            elif ex.tipo == Tipos.FUNCTION:
                val = val[2]
            elif ex.tipo == Tipos.BOOLEAN:
                val = str(val).lower()
            if tamaño == len(self.expresion):
                valor += str(val)
            else:
                valor += str(val) + ' '
            
            tamaño+=1

        arbol_.updateConsola(valor+"\n")
    
    def getStruct(self, val, struct):
        val += struct[1] + "("
        lista = list(struct.keys())
        for key in lista:
            if key == 1 or key == 2:
                continue
            if key != lista[2]:
                val +=","
            valor = struct[key]
            if valor[1] == Tipos.OBJECT:
                val = self.getStruct(val, valor[0])
            elif valor[1] == Tipos.ARRAY:
                val = str(self.getArrayValue(valor[0], val))
            elif valor[1] == Tipos.STRING:
                val +='"'+valor[0]+'"'
            elif valor[1] == Tipos.BOOLEAN:
                val += str(valor[0]).lower()
            elif valor[1].tipo == Tipos.FUNCTION:
                val = valor[2]
            else:
                val += str(valor[0])
        val += ")"
        return val
    
    def getArrayValue(self, simb, val):
        val += '['
        for sim in simb:
            if sim != simb[0]:
                val+=","
            if not isinstance(sim, Simbolo):
                val = self.getArrayValue(sim, val)
            else:
                valor = sim.getValor()
                if sim.getTipo() == Tipos.OBJECT:
                    val = self.getStruct(val, valor)
                else:
                    if sim.getTipo() == Tipos.STRING:
                        val +='"'+valor+'"'
                    elif sim.getTipo() == Tipos.FUNCTION:
                        val = valor[2]
                    elif sim.getTipo() == Tipos.BOOLEAN:
                        val = str(valor).lower()
                    else:
                        val+=str(valor)
        val += ']'
        return val
        
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('CONSOLE.LOG')
        nodo.addHijo('CONSOLE.LOG')
        nodo.addHijo('(')
        anterior = None
        nodoParametro = None
        for ex in self.expresion:
            nodoParametro = NodeAST("PARAMETROS")
            if anterior is not None:
                nodoParametro.addHijoNodo(anterior)
                nodoParametro.addHijo(',')
            nodoParametro.addHijoNodo(ex.getNodo())
            anterior = nodoParametro
        if nodoParametro is not None:
            nodo.addHijoNodo(nodoParametro)
        nodo.addHijo(')')
        return nodo