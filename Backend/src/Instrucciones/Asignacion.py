from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.Error import Error
from ..Helpers.TiposDatos import Tipos
from datetime import datetime

class Asignacion(Abstracta):
    def __init__(self, identificador, valor, fila, columna):
        self.identificador = identificador
        self.valor = valor
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getSimbolo(self.identificador)
        simb = tabla.getObjeto(self.identificador)
        if simbolo == None and simb == None: return Error('Semantico', 'No se puede actualizar, la variable'+ self.identificador + ' no existe',self.fila, self.columna,datetime.now().date())
        nuevoValor = self.valor.interpretar(arbol, tabla)
        if simbolo!= None:
            if simbolo.getTipo() == Tipos.BOOLEAN:
                if isinstance(nuevoValor, bool):
                    simbolo.setValor(nuevoValor)
                    tabla.actualizarSimbolo(simbolo)
            elif simbolo.getTipo() == Tipos.STRING:
                if isinstance(nuevoValor, str):
                    simbolo.setValor(nuevoValor)
                    tabla.actualizarSimbolo(simbolo)
            elif simbolo.getTipo() == Tipos.NUMBER:
                if (isinstance(nuevoValor, int) or isinstance(nuevoValor, float)) and (not isinstance(nuevoValor, bool)) :
                    # if nuevoValor == True or nuevoValor == False:
                    #     return Error('Semantico','No es posible actualizar la variable',self.fila, self.columna)
                    simbolo.setValor(nuevoValor)
                    tabla.actualizarSimbolo(simbolo)
            elif simbolo.getTipo() == Tipos.ANY:
                simbolo.setValor(nuevoValor)
                tabla.actualizarSimbolo(simbolo)
            else:
                return Error('Semantico', 'El valor no corresponde al tipo de dato: '+simbolo.getTipo(),self.fila, self.columna, datetime.now().date())
        elif simb != None: 
            simb.setAtributos(nuevoValor)
            tabla.actualizarObjeto(simb)
    def traducir(self, arbol, tabla):
        pass