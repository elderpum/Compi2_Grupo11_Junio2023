from Abstracto.instruccion import Instruccion
from Tabla.Simbolo import Simbolo
from Tabla.Nodo_list import Node_list
from Tabla.NodeAST import NodeAST
from Tabla.Arbol import Arbol
from Tabla.Tabla_simbolos import TablaSimbolo
from Tabla.Tipo import  Tipos
from Tabla.Errores import Error
from .break_ import BREAK
from .continue_ import CONTINUE
from .return_ import RETURN

class ForNorm(Instruccion):

    def __init__(self, inicio_, expresion_, contador_, Instruccion_, fila_, columna_):
        super().__init__(Tipos.ANY, fila_, columna_)
        self.inicio = inicio_
        self.expresion = expresion_
        self.contador = contador_
        self.instruciones = Instruccion_
    
    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        nuevaTabla = TablaSimbolo(tabla_)  # NUEVO ENTORNO

        inicio = self.inicio.Ejecutar(arbol_, nuevaTabla)
        if isinstance(inicio, Error): return inicio

        condicion = self.expresion.Ejecutar(arbol_, nuevaTabla)
        if isinstance(condicion, Error): return condicion
        # Validar que el tipo sea booleano
        if self.condicion.tipo != 'boolean':
            return Error("Semantico", "Tipo de dato no booleano en FOR.", self.fila, self.columna)
        # Recorriendo las instrucciones
        while condicion:
            for instruccion in self.bloqueFor:
                result = instruccion.Ejecutar(arbol_, nuevaTabla)
                if isinstance(result, Error):
                    arbol_.excepciones.append(result)
            
            nuevo_valor = self.contador.Ejecutar(arbol_, nuevaTabla)
            if isinstance(nuevo_valor, Error): return nuevo_valor
            
            simbolo = Simbolo(self.inicio.id, self.inicio, nuevo_valor, self.fila, self.columna)

            # Actualizando el valor de la variable en la tabla de simbolos
            valor = nuevaTabla.updateTabla(simbolo)

            if isinstance(valor, Error): return valor

            condicion = self.expresion.Ejecutar(arbol_, nuevaTabla)
            if isinstance(condicion, Error): return condicion
            if self.condicion.tipo != 'boolean':
                return Error("Semantico", "Tipo de dato no booleano en FOR.", self.fila, self.columna)
        return None
            
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