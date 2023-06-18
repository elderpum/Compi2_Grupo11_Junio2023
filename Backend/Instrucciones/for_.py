from ..Abstracto.instruccion import Instruccion
from ..Tabla.Simbolo import Simbolo
from ..Tabla.Nodo_list import Node_list
from ..Tabla.NodeAST import NodeAST
from ..Tabla.Arbol import Arbol
from ..Tabla.Tabla_simbolos import TablaSimbolo
from ..Tabla.Tipo import  Tipos
from ..Tabla.Errores import Error
from .break_ import BREAK
from .continue_ import CONTINUE
from .return_ import RETURN

class FOR(Instruccion):

    def __init__(self, id_, expresion_, instruciones_,fila_, columna_):
        super().__init__(Tipos.ANY, fila_, columna_)
        self.id = id_
        self.expresion = expresion_
        self.instruciones = instruciones_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        variable = tabla_.getVariable(self.id)
        arbol_.PilaCiclo.append("FOR")
        tip = None
        ciclo = self.expresion.Ejecutar(arbol_, tabla_)
        if isinstance(ciclo, Error): 
            arbol_.PilaCiclo.pop()
            return ciclo
        if self.expresion.tipo == Tipos.STRING:
            tip = Tipos.STRING
            data = ciclo
        elif self.expresion.tipo == Tipos.ARRAY:
            data = ciclo
        elif self.expresion.tipo == Tipos.RANGE:
            if ciclo[0] == None:
                arbol_.PilaCiclo.pop()
                return Error("Sintactico","Rango no invalido para el ciclo for", self.fila, self.columna)
            inicial = ciclo[0]
            final = ciclo[1]
            distancia = final-inicial
            tip = Tipos.NUMBER
            if type(inicial) == type(0.1) or type(final) == type(0.1):
                tip = Tipos.NUMBER
            data = range(0,int(distancia)+1)            
        else:
            arbol_.PilaCiclo.pop()
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
            nuevaTabla = TablaSimbolo(tabla_, "FOR")
            nuevaTabla.funcion = tabla_.funcion
            arbol_.Lista_Simbolo.Agregar(Node_list(self.id, variable.getTipo(), nuevaTabla.Entorno, self.fila, self.columna))
            nuevaTabla.setVariable(variable)
            for ins in self.instruciones:
                res = ins.Ejecutar(arbol_, nuevaTabla)
                if isinstance(res, Error) and not evaluado:
                    arbol_.errores.append(res)
                elif isinstance(res, RETURN):
                    arbol_.PilaCiclo.pop()
                    return res
                elif isinstance(res, BREAK):
                    arbol_.PilaCiclo.pop()
                    return True
                elif isinstance(res, CONTINUE):
                    break
            evaluado = True
        arbol_.PilaCiclo.pop()
        
        return True
        
def getNodo(self) -> NodeAST:
    nodo = NodeAST('FOR')
    nodo.addHijoNodo(self.expresion.getNodo())
    inst = NodeAST('INSTRUCCIONES')
    for ins in self.instruciones:
        instr = NodeAST("INSTRUCCION")
        instr.addHijoNodo(ins.getNodo())
        inst.addHijoNodo(instr)
    nodo.addHijoNodo(inst)
    return nodo