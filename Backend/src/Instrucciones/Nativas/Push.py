from ...Abstracta.Abstracta import Abstracta
from ...TablaSimbolos.TablaSimbolos import TablaSimbolos
from ...TablaSimbolos.Error import Error
from ...Helpers.TiposDatos import Tipos
from ...Expresiones.Primitivas import Primitivas
from datetime import datetime

class Push(Abstracta):
    def __init__(self,identificador, valorNuevo, fila, columna):
        self.identificador = identificador
        self.valorNuevo = valorNuevo
        self.tipo = Tipos.ANY
        super().__init__(fila, columna)
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getSimbolo(self.identificador)
        if simbolo == None: return Error('Sintactico','La variable no esta definida', self.fila, self.columna,datetime.now().date())
        if isinstance(simbolo.getValor(), list):
            if isinstance(self.valorNuevo, list):
                listado = []
                for valor in self.valorNuevo:
                    value = valor.interpretar(arbol,tabla)
                    if isinstance(value,Error): return value
                    if simbolo.getTipo () == valor.getTipo():
                        listado.append(value)
                    elif simbolo.getTipo() == Tipos.ANY:
                        listado.append(value)
                    else:
                        return Error('Semantico', 'No se puede agregar '+str(self.valorNuevo.getTipo())+" a un ARRAY tipo: "+str(simbolo.getTipo()) ,self.fila, self.columna, datetime.now().date())
                simbolo.getValor().append(listado)
                tabla.actualizarSimbolo(simbolo)
                return None
            else:
                nuevo = self.valorNuevo.interpretar(arbol, tabla)
                if self.valorNuevo.getTipo() == simbolo.getTipo():
                    simbolo.getValor().append(nuevo)
                    tabla.actualizarSimbolo(simbolo)
                    return None
                elif simbolo.getTipo() == Tipos.ANY:
                    simbolo.getValor().append(nuevo)
                    tabla.actualizarSimbolo(simbolo)
                    return None
                else:
                    return Error('Semantico', 'No se puede agregar '+str(self.valorNuevo.getTipo())+" a un ARRAY tipo: "+str(simbolo.getTipo()) ,self.fila, self.columna, datetime.now().date())
        else: 
            return Error('Semantico', 'El identificador debe ser un ARRAY',self.fila, self.columna, datetime.now().date())
        
    def traducir(self, arbol, tabla):
        pass