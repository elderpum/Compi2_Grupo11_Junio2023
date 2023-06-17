from ..Abstracto.instruccion import Instruccion
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Tipo import  Tipos
from ..Tabla.Errores import Error
from .break_ import BREAK
from .continue_ import CONTINUE
from .return_ import RETURN

class FOR(Instruccion):

    def __init__(self, id, expresion, instruciones,fila, columna):
        super().__init__(Tipos.ANY, fila, columna)
        self.id = id
        self.expresion = expresion
        self.instruciones = instruciones

    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        variable = tabla.getVariable(self.id)
        arbol.PilaCiclo.append("FOR")
        tip = None
        ciclo = self.expresion.Ejecutar(arbol, tabla)
        if isinstance(ciclo, Error): 
            arbol.PilaCiclo.pop()
            return ciclo
        if self.expresion.tipo == Tipos.STRING:
            tip = Tipos.STRING
            data = ciclo
        elif self.expresion.tipo == Tipos.ARRAY:
            data = ciclo
        elif self.expresion.tipo == Tipos.RANGE:
            if ciclo[0] == None:
                arbol.PilaCiclo.pop()
                return Error("Sintactico","Rango no recorrible por el ciclo for", self.fila, self.columna)
            inicial = ciclo[0]
            final = ciclo[1]
            distancia = final-inicial
            tip = Tipos.ENTERO
            if type(inicial) == type(2.1) or type(final) == type(2.1):
                tip = Tipos.FLOAT
            data = range(0,int(distancia)+1)
        elif self.expresion.tipo == Tipos.ENTERO or self.expresion.tipo == Tipos.FLOAT:
            inicial = ciclo
            final = ciclo
            distancia = final-inicial
            tip = Tipos.ENTERO
            if type(inicial) == type(2.1) or type(final) == type(2.1):
                tip = Tipos.FLOAT
            self.expresion.tipo = Tipos.RANGE
            data = range(0,int(distancia)+1)
            
        else:
            arbol.PilaCiclo.pop()
            return Error("Semantico","El for no puede efectuarse con el tipo "+str(self.expresion.tipo.value), self.fila, self.columna)
        evaluado = False
        for a in data:
            if variable == None:
                variable = Simbolo(None,tip, self.id, self.fila, self.columna)
            if self.expresion.tipo==Tipos.RANGE:
                variable.setValor(inicial+a)
            elif self.expresion.tipo == Tipos.ARRAY:
                if isinstance(a, Simbolo):
                    variable.setTipo(a.getTipo())
                    variable.setValor(a.getValor())
                else:
                    variable.setTipo(Tipos.ARRAY)
                    variable.setValor(a)
            else:
                variable.setValor(a)
            nuevaTabla = Tabla_Simbolo(tabla, "FOR")
            nuevaTabla.funcion = tabla.funcion
            arbol.Lista_Simbolo.Agregar(Lista_Simbolo(self.id, variable.getTipo(), nuevaTabla.Entorno, self.fila, self.columna))
            nuevaTabla.setVariable(variable)
            for ins in self.instruciones:
                res = ins.Ejecutar(arbol, nuevaTabla)
                if isinstance(res, Error) and not evaluado:
                    arbol.errores.append(res)
                elif isinstance(res, RETURN):
                    arbol.PilaCiclo.pop()
                    return res
                elif isinstance(res, BREAK):
                    arbol.PilaCiclo.pop()
                    return True
                elif isinstance(res, CONTINUE):
                    break
            evaluado = True
        arbol.PilaCiclo.pop()
        
        return True
        
    def getNodo(self) -> NodoAST:
        nodo = NodoAST('FOR')
        nodo.agregarHijo(self.id)
        nodo.agregarHijoNodo(self.expresion.getNodo())
        inst = NodoAST('INSTRUCCIONES')
        for ins in self.instruciones:
            insts = NodoAST("INSTRUCCION")
            insts.agregarHijoNodo(ins.getNodo())
            inst.agregarHijoNodo(insts)
        nodo.agregarHijoNodo(inst)
        return nodo