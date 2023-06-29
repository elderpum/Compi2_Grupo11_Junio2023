from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta
from ..Helpers.TiposDatos import Tipos
from datetime import datetime

class AccesoArray(Abstracta):
    def __init__(self,identificador, indice, fila, columna):
        self.identificador = identificador
        self.indice = indice
        self.tipo = None
        super().__init__(fila, columna)
        
    def getTipo(self):
        return self.tipo
    def setTipo(self, tipo):
        self.tipo = tipo
    def interpretar(self,arbol, tabla):
        simbolo = tabla.getSimbolo(self.identificador)
        
        self.setTipo(simbolo.getTipo())
        if isinstance(simbolo.getValor(),list) and len(simbolo.getValor())>1:
            if isinstance(self.indice, list) and len(self.indice)>1:
                inde = self.indice[0].interpretar(arbol,tabla)
                if self.indice[0].getTipo() == Tipos.NUMBER: 
                    inde = self.indice[0].interpretar(arbol,tabla)
                    if isinstance(inde,Error): return inde
                    if isinstance(inde,int):
                        if 0<= inde and inde< len(simbolo.getValor()):
                            #
                            #(len(simbolo.getValor()))>inde and inde>=0
                            nuevos = simbolo.getValor()[inde]
                            if isinstance(nuevos, list):
                                indei = self.indice[1].interpretar(arbol,tabla)
                                if isinstance(indei,Error): return indei
                                if isinstance(indei, int):
                                    if 0<= indei and indei< len(nuevos):
                                        return nuevos[indei]
                                    else:
                                        return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                                elif self.indice[1].getTipo() == Tipos.Any:
                                    if isinstance(inde,int):
                                        if 0<= indei and indei< len(nuevos):
                                            return nuevos[indei]
                                        else:
                                            return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                                else: 
                                    return Error('Semantico', 'El indice debe ser entero', self.fila, self.columna,datetime.now().date())
                            else: 
                                return Error('Semantico', 'El objeto no es un ARRAY', self.fila, self.columna,datetime.now().date())
                        else:
                            return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                    else:
                        return Error('Semantico', 'El indice debe ser entero', self.fila, self.columna,datetime.now().date())
                elif self.indice[0].getTipo() == Tipos.ANY: 
                    if  isinstance(inde,int) and not isinstance(inde,bool):
                        inde = self.indice[0].interpretar(arbol,tabla)
                        if isinstance(inde,Error): return inde
                        if isinstance(inde,int):
                            if (len(simbolo.getValor()))>inde and inde>=0:
                                #
                                nuevos = simbolo.getValor()[inde]
                                if isinstance(nuevos, list):
                                    indei = self.indice[1].interpretar(arbol,tabla)
                                    if isinstance(indei,Error): return indei
                                    if isinstance(indei, int):
                                        if 0<= indei and indei< len(nuevos):
                                            return nuevos[indei]
                                        else:
                                            return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                                    elif self.indice[1].getTipo() == Tipos.Any:
                                        if isinstance(inde,int):
                                            if 0<= indei and indei< len(nuevos):
                                                return nuevos[indei]
                                            else:
                                                return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                                    else: 
                                        return Error('Semantico', 'El indice debe ser entero', self.fila, self.columna,datetime.now().date())
                                else: 
                                    return Error('Semantico', 'El objeto no es un ARRAY', self.fila, self.columna,datetime.now().date())
                                #
                            else:
                                return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                        else:
                            return Error('Semantico', 'El indice debe ser entero', self.fila, self.columna,datetime.now().date())
                else:
                    return Error('Semantico', 'Tipo de dato en el indice erroneo debe ser NUMBER, se recibio: '+ str(self.indice.getTipo()), self.fila, self.columna,datetime.now().date())
            else:
                inde = self.indice[0].interpretar(arbol,tabla)
                if self.indice[0].getTipo() == Tipos.NUMBER: 
                    inde = self.indice[0].interpretar(arbol,tabla)
                    if isinstance(inde,Error): return inde
                    if isinstance(inde,int):
                        if 0<= inde and inde< len(simbolo.getValor()):
                            #
                            #(len(simbolo.getValor()))>inde and inde>=0
                            return simbolo.getValor()[inde]
                        else:
                            return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                    else:
                        return Error('Semantico', 'El indice debe ser entero', self.fila, self.columna,datetime.now().date())
                elif self.indice[0].getTipo() == Tipos.ANY: 
                    if  isinstance(inde,int) and not isinstance(inde,bool):
                        inde = self.indice[0].interpretar(arbol,tabla)
                        if isinstance(inde,Error): return inde
                        if isinstance(inde,int):
                            if (len(simbolo.getValor()))>inde and inde>=0:
                                return simbolo.getValor()[inde]
                            else:
                                return Error('Semantico', 'Indice fuera de tamano', self.fila, self.columna,datetime.now().date())
                        else:
                            return Error('Semantico', 'El indice debe ser entero', self.fila, self.columna,datetime.now().date())
                elif self.indice[0].getTipo() == None:
                    if  isinstance(inde,int) and not isinstance(inde,bool):
                        inde = self.indice[0].interpretar(arbol,tabla)
                        if isinstance(inde,Error): return inde
                        if isinstance(inde,int):
                            if (len(simbolo.getValor()))>inde and inde>=0:
                                return simbolo.getValor()[inde]
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