from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta
from ..Helpers.TiposDatos import Tipos
from ..TablaSimbolos.Traductor import Traductor
from ..Helpers.ReturnCo import ReturnCo
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
        auxGen = Traductor()
        traductor = auxGen.obtenerInstancia()
        traductor.nuevoComentario("Acceso a la variable " + self.identificador)
        var = ''
        if self.identificador:
            var = tabla.getSimbolo3(self.identificador)
            if var == None:
                traductor.nuevoComentario("Fin de compilacion de Acceso por error")
                return Error("Semantico", "Variable no encontrada", self.fila, self.columna,datetime.now().date())
        else:
            var = ''
        traductor.manejoError()
        temp = traductor.agregarTemporal()
        tempPos = var.posicion
        if not var.isGlobal:
            tempPos = traductor.agregarTemporal()
            traductor.agregarExpresion(tempPos, 'P', var.pos, "+")
        traductor.getStack(temp, tempPos)
        x = 0
        tipo = var.getTipo()
        tipoAux = var.getTipoAux()
        for value in self.indice:
            x += 1
            tmp3 = traductor.agregarTemporal()
            tmp4 = traductor.agregarTemporal()
            tmp5 = traductor.agregarTemporal()
            Lbl1 = traductor.nuevaEtiqueta()
            Lbl2 = traductor.nuevaEtiqueta()
            Lbl3 = traductor.nuevaEtiqueta()

            indice = value.traducir(arbol, tabla)
            traductor.agregarExpresion(tmp3, temp, indice.getValue(), "+")

            traductor.agregarIf(indice.getValue(),'1','<',Lbl1) #Agregado
            traductor.getHeap(tmp5, temp)
            traductor.agregarIf(indice.getValue(),tmp5,'>', Lbl1) #Agregado
            traductor.agregarGoto(Lbl2)
            traductor.colocarEtiqueta(Lbl1)
            traductor.llamarFun('BoundsError')
            traductor.agregarGoto(Lbl3)
            traductor.colocarEtiqueta(Lbl2)

            traductor.getHeap(tmp4, tmp3)

            traductor.agregarGoto(Lbl3)
            traductor.putLabel(Lbl3)

            temp = tmp4
            if x == len(self.indice):
                var.setTipo(var.getTipoAux())
            else:
                if isinstance(var.getTipoAux(), list):
                    var.setTipo(var.getTipoAux()[0])
                    var.setTipoAux(var.getTipoAux()[1])
                else:
                    return Error("Semantico", "No se puede acceder al arreglo", self.fila, self.colum)
        traductor.nuevoComentario(f'Fin compilacion de acceso de la variable {self.id}')
        space = ReturnCo(tmp4, var.getTipo(), True, var.getTipoAux())
        var.setTipo(tipo)
        var.setTipoAux(tipoAux)
        return space