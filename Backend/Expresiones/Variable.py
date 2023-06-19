import re
from ..Abstracto.instruccion import Instruccion
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Simbolo import Simbolo
from ..Tabla.Tipo import Tipos
from ..Tabla.Errores import Error

class Variable(Instruccion):

    def __init__(self, id1_, fila_, columna_, id2_=None, posiciones_ = None):
        super().__init__(Tipos.NOTHING, fila_, columna_)
        self.id1 = id1_
        self.id2= id2_
        self.posiciones = posiciones_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        if self.id2 == None:
            variable = tabla_.getVariable(self.id)
            if variable is not None:
                self.tipo = variable.getTipo()
                if self.tipo == Tipos.ARRAY:
                    if self.posiciones is not None:
                        try:
                            val = self.getArray(variable.getValor(), arbol_, tabla_)
                            if isinstance(val, Error): return val
                            if isinstance(val, Simbolo):
                                self.tipo = val.getTipo()
                                return val.getValor()
                            else:
                                self.tipo = Tipos.ARRAY
                                return val
                        except:
                            return Error("Sintactico","Posicion de Array fuera de rango", self.fila, self.columna)
                    else:
                        return variable.getValor()
                elif self.posiciones is not None:
                    return Error("Sintactico","La variable indicada no es un array", self.fila, self.columna)
                else:
                    return variable.getValor()
            else:
                return Error("Semantico", "La variable indicada no existe", self.fila, self.columna)
        else:       
            variable = self.id.Ejecutar(arbol_, tabla_)
            if isinstance(variable, Error):return variable
            self.tipo = self.id.tipo
            if self.tipo!=Tipos.OBJECT:
                return Error("Semantico","La variable indicada no corresponde a un objeto struct", self.fila, self.columna)
            try:
                get = variable[self.id2]
                self.tipo = get[1]
                if self.posiciones == None:
                    return get[0]
                else:
                    ress = self.getArray(get[0], arbol_, tabla_)
                    if isinstance(ress, Error): return ress
                    if isinstance(ress, Simbolo):
                        self.tipo = ress.getTipo()
                        return ress.getValor()
                    else:
                        self.tipo = Tipos.ARRAY
                        return ress
            except:
                return Error("Sintactico","La propiedad "+self.id2+" No existe en el struct indicado", self.fila, self.columna)
    
    def getArray(self, array_, arbol_, tabla_):
        data = array_
        for posicion in self.posiciones:
            res = posicion.Ejecutar(arbol_, tabla_)
            if isinstance(res, Error):return res
            if posicion.tipo != Tipos.NUMBER and posicion.tipo!= Tipos.RANGE:
                return Error("Sintactico","La posición del array debe ser un numero", self.fila, self.columna)
            
            if posicion.tipo == Tipos.NUMBER:
                res-=1
                if res < 0:
                    return Error("Sintactico","Posición de Array fuera de rango",self.fila, self.columna)
                data = data[res]
        return data
        
    def clonarSimbolos(self, array, izquierda, derecha):
        array2 = None
        if izquierda != None and derecha!=None:
            izquierda -=1
            derecha -=1
            if izquierda <0 or derecha<0:
                return Error("Sintactico", "Valor fuera de rango del array", self.fila, self.columna)
            array2 = array[izquierda:derecha+1]
        else:
            array2 = array[:]
        newarray = []
        for sim in array2:
            if isinstance(sim, Simbolo):
                newarray.append(Simbolo(sim.valor, sim.tipo, "", sim.fila, sim.columna))
            else:
                newarray.append(sim)
        return newarray
              
            
    
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('VARIABLE')
        id = NodeAST("ID")
        if self.id2 == None:
            id.addHijo(self.id)
            nodo.addHijoNodo(id)
        else:
            nodo.addHijoNodo(self.id.getNodo())
            id2 = NodeAST("ID")
            nodo.addHijo(".")
            id2.addHijo(self.id2)
            nodo.addHijoNodo(id2)
            if self.posiciones is not None:
                anterior_pos = None
                nodo_posicion = None
                for pos in self.posiciones:
                    nodo_posicion = NodeAST("LISTA_ARRAY")
                    if anterior_pos is not None:
                        nodo_posicion.addHijoNodo(anterior_pos)
                    nodo_posicion.addHijo("[")
                    nodo_posicion.addHijoNodo(pos.getNodo())
                    nodo_posicion.addHijo("]")
                    anterior_pos = nodo_posicion
                nodo.addHijoNodo(nodo_posicion)
        return nodo