from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.Error import Error
from ..Helpers.TiposDatos import Tipos
from datetime import datetime

class AsignacionArreglo(Abstracta):
    def __init__(self,identificador, indice, valor, fila, columna):
        self.identificador = identificador
        self.indice = indice
        self.valor = valor
        super().__init__(fila, columna)
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getSimbolo(self.identificador)
        if simbolo == None: return Error('Sintactico','La variable no esta definida '+str(self.identificador), self.fila, self.columna,datetime.now().date())
        if isinstance(simbolo.getValor(),list):
            if isinstance(self.indice, list) and len(self.indice)>1:
                ind = self.indice[0].interpretar(arbol,tabla)
                valo = simbolo.getValor()[ind]
                if isinstance(valo,list):
                    indi = self.indice[1].interpretar(arbol,tabla)
                    if 0<= indi and indi<len(valo):
                        nuevoValor = self.valor.interpretar(arbol,tabla)
                        if simbolo.getTipo() == self.valor.getTipo():
                            valo[indi] = nuevoValor
                            tabla.actualizarSimbolo(simbolo)
                            return None
                        elif simbolo.getTipo() == Tipos.ANY:
                            valo[indi] = nuevoValor
                            tabla.actualizarSimbolo(simbolo)
                            return None
                        else:
                            return Error('Semantico', 'El valor no puede ser almacenado en el arreglo de tipo '+str(simbolo.getTipo()), self.fila, self.columna,datetime.now().date())
                    else:
                        return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                else:
                    return Error('Semantico', 'La variable no es un arreglo', self.fila, self.columna,datetime.now().date())
            else:
                inde = self.indice[0].interpretar(arbol,tabla)
                if self.indice[0].getTipo() == Tipos.NUMBER: 
                    inde = self.indice[0].interpretar(arbol,tabla)
                    if isinstance(inde,Error): return inde
                    if isinstance(inde,int):
                        if (len(simbolo.getValor()))>inde and inde>=0:
                            nuevoValor = self.valor.interpretar(arbol,tabla)
                            if simbolo.getTipo() == self.valor.getTipo():
                                simbolo.getValor()[inde] = nuevoValor
                                tabla.actualizarSimbolo(simbolo)
                                return None
                            elif simbolo.getTipo() == Tipos.ANY:
                                simbolo.getValor()[inde] = nuevoValor
                                tabla.actualizarSimbolo(simbolo)
                                return None
                            else:
                                return Error('Semantico', 'El valor no puede ser almacenado en el arreglo de tipo '+str(simbolo.getTipo()), self.fila, self.columna,datetime.now().date())
                        else:
                            return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                    else:
                        return Error('Semantico', 'El indice debe ser entero', self.fila, self.columna,datetime.now().date())
                elif self.indice[0].getTipo() == Tipos.ANY: 
                    inde = self.indice[0].interpretar(arbol,tabla)
                    if isinstance(inde,Error): return inde
                    if isinstance(inde,int):
                        if (len(simbolo.getValor()))>inde and inde>=0:
                            nuevoValor = self.valor.interpretar(arbol,tabla)
                            if simbolo.getTipo() == self.valor.getTipo():
                                simbolo.getValor()[inde] = nuevoValor
                                tabla.actualizarSimbolo(simbolo)
                                return None
                            elif simbolo.getTipo() == Tipos.ANY:
                                simbolo.getValor()[inde] = nuevoValor
                                tabla.actualizarSimbolo(simbolo)
                                return None
                            else:
                                return Error('Semantico', 'El valor no puede ser almacenado en el arreglo de tipo '+str(simbolo.getTipo()), self.fila, self.columna,datetime.now().date())
                        else:
                            return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                    else:
                        return Error('Semantico', 'El indice debe ser entero', self.fila, self.columna,datetime.now().date())
                else:
                    return Error('Semantico', 'Tipo de dato en el indice erroneo debe ser NUMBER, se recibio: '+ str(self.indice[0].getTipo()), self.fila, self.columna,datetime.now().date())
        else:
            return Error('Semantico', 'La variable no es un arreglo', self.fila, self.columna,datetime.now().date())    
    def traducir(self, arbol, tabla):
        pass