from Abstracto.instruccion import Instruccion
from Tabla.NodeAST import NodeAST
from Tabla.Arbol import Arbol
from Tabla.Tabla_simbolos import TablaSimbolo
from Tabla.Tipo import  Tipos
from Tabla.Errores import Error
from .break_ import BREAK
from .continue_ import CONTINUE
from .return_ import RETURN

class WHILE(Instruccion):

    def __init__(self, expresion_, instruciones_,fila_, columna_):
        super().__init__(Tipos.ANY, fila_, columna_)
        self.expresion = expresion_
        self.instruciones = instruciones_

    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        condicion = self.expresion.Ejecutar(arbol_, tabla_)
        if isinstance(condicion, Error): 
            arbol_.PilaCiclo.pop()
            return condicion
        arbol_.PilaCiclo.append("WHILE")
        if self.expresion.tipo == Tipos.BOOLEAN:
            evaluado = False
            while condicion:
                nuevo_entorno = TablaSimbolo(tabla_, "WHILE")
                for inst in self.instruciones:
                    res = inst.Ejecutar(arbol_, nuevo_entorno)
                    if isinstance(res, Error) and evaluado:
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
                condicion = self.expresion.Ejecutar(arbol_, tabla_)
                if isinstance(condicion, Error): return condicion
            arbol_.PilaCiclo.pop() 
            return True    
        else:
            arbol_.PilaCiclo.pop()
            return Error("Sintactico", "Se esperaba un valor booleano en la expresion del while", self.fila, self.columna)
                    
        
    def getNodo(self) -> NodeAST:
        nodo = NodeAST('WHILE')
        nodo.addHijoNodo(self.expresion.getNodo())
        inst = NodeAST('INSTRUCCIONES')
        for ins in self.instruciones:
            instr = NodeAST("INSTRUCCION")
            instr.addHijoNodo(ins.getNodo())
            inst.addHijoNodo(instr)
        nodo.addHijoNodo(inst)
        return nodo