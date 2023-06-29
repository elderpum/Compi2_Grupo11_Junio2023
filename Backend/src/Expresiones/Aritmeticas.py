import math
from ..Abstracta.Abstracta import Abstracta
from ..Helpers.TipoOperacionesAritmeticas import Operacion
from ..Helpers.TiposDatos import Tipos
from .Identificador import Identificador
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.Traductor import Traductor
from ..Instrucciones.LlamadaFunciones import LlamadaFuncion

class Aritmeticas(Abstracta):
    def __init__(self,operadorIzq,operadorDere, operacion, fila, columna):
        self.operadorDere = operadorDere
        self.operadorIzq = operadorIzq
        self.operacion = operacion
        self.tipo = None
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        izq = None if self.operadorIzq == None else self.operadorIzq.interpretar(arbol, tabla)
        tipoIzq = None if self.operadorIzq == None else self.operadorIzq.getTipo()
        dere = self.operadorDere.interpretar(arbol, tabla)
        if isinstance(izq,Error): return izq
        if isinstance(dere,Error): return dere
        tipoDere = self.operadorDere.getTipo()
        if self.operacion == Operacion.SUMA:
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.NUMBER
                return izq + dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.STRING:
                self.tipo = Tipos.STRING
                return izq + dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if isinstance(izq,str) and isinstance(dere,str):
                    return izq + dere
                elif (isinstance(izq,int) or isinstance(izq,float))and (isinstance(dere,int) or isinstance(dere,float)):
                    return izq + dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return izq + dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return izq + dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.STRING:
                self.tipo = Tipos.ANY
                if isinstance(izq,str) :
                    return izq + dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if isinstance(dere,str) :
                    return izq + dere
            else: 
                return 'Error: Tipos de datos no validos para suma' # manejar error
        elif self.operacion == Operacion.RESTA:
            if tipoIzq == None and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.NUMBER
                return - dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.NUMBER
                return izq - dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float))and (isinstance(dere,int) or isinstance(dere,float)):
                    return izq - dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return izq - dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return izq - dere
            else:
                return 'Error: Tipos de datos no validos para resta' # manejar error
        elif self.operacion == Operacion.MULTI:
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.NUMBER
                return izq * dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float))and (isinstance(dere,int) or isinstance(dere,float)):
                    return izq * dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return izq * dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return izq * dere
            else:
                return 'Error: Tipos de datos no validos para multiplicacion' # manejar error
        elif self.operacion == Operacion.DIV:
            if dere == 0:
                    return 'Error: No es posible dividir entre 0'
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.NUMBER
                return izq / dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float))and (isinstance(dere,int) or isinstance(dere,float)):
                    return izq / dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return izq / dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return izq / dere
            else:
                return 'Error: Tipos de datos no validos para division' # manejar error
        elif self.operacion == Operacion.POTENCIA:
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.NUMBER
                return pow(izq,dere)
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float))and (isinstance(dere,int) or isinstance(dere,float)):
                    return pow(izq,dere)
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return pow(izq,dere)
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return pow(izq,dere)
            else:
                return 'Error: Tipos de datos no validos para potencia' # manejar error
        elif self.operacion == Operacion.MODULO:
            if dere == 0:
                    return 'Error: No es posible dividir entre 0'
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.NUMBER
                div =math.trunc(izq/dere) 
                return izq-(dere*div)
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float))and (isinstance(dere,int) or isinstance(dere,float)):
                    div =math.trunc(izq/dere) 
                    return izq-(dere*div)
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                self.tipo = Tipos.ANY
                if (isinstance(izq,int) or isinstance(izq,float)):
                    div =math.trunc(izq/dere) 
                    return izq-(dere*div)
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                self.tipo = Tipos.ANY
                if (isinstance(dere,int) or isinstance(dere,float)):
                    div =math.trunc(izq/dere) 
                    return izq-(dere*div)
            else:
                return 'Error: Tipos de datos no validos para Modulo' # manejar error
        elif self.operacion == Operacion.INCREMENTO:
            if tipoIzq == None and tipoDere == Tipos.NUMBER:
                # if isinstance(dere,Identificador):
                #     simbolo = tabla.getSimbolo(dere.identificador)
                #     simbolo.setValor(simbolo.getValor()+1)
                #     tabla.actualizarSimbolo(simbolo)
                return dere+1
            elif tipoIzq == None and tipoDere == Tipos.ANY:
                if isinstance(dere, int) or isinstance(dere,float):
                    return dere+1
        elif self.operacion == Operacion.DECREMENTO:
            if tipoIzq == None and tipoDere == Tipos.NUMBER:
                return dere-1
            elif tipoIzq == None and tipoDere == Tipos.ANY:
                if isinstance(dere, int) or isinstance(dere,float):
                    return dere-1
    def getTipo(self):
        return self.tipo
    def traducir(self, arbol, tabla):
        genAux = Traductor()
        generador = genAux.obtenerInstancia()
        temporal = ''
        operador = ''
        der = ''
        izq = self.operadorIzq.interpretar(arbol, tabla)
        if isinstance(izq,Error): return izq
        if isinstance(self.operadorDere, LlamadaFuncion): 
            self.operadorDere.guardarTemps(generador,tabla, [izq])
            der = self.operadorDere.interpretar(arbol,tabla)
            if isinstance(der,Error): return der
            self.operadorDere.recuperarTemps(generador, tabla,[izq])
        else:
            der = self.operadorDere.interpretar(arbol, tabla)
            if isinstance(der, Error): return der
            
        if self.operacion == Operacion.SUMA:
            operador = '+'
            temporal = generador.agregarTemporal()
            generador.agregarExpresion(temporal,izq,der,operador)
            self.tipo = Tipos.NUMBER
            return temporal
        elif self.operacion == Operacion.RESTA:
            operador = '-'
            temporal = generador.agregarTemporal()
            generador.agregarExpresion(temporal, izq, der, operador)
            self.tipo = Tipos.NUMBER
            return temporal
        elif self.operacion == Operacion.MULTI:
            operador = '*'
            temporal = generador.agregarTemporal()
            generador.agregarExpresion(temporal, izq, der, operador)
            self.tipo = Tipos.NUMBER
            return temporal
        elif self.operacion == Operacion.DIV:
            if der == 0:
                return 'Error: Division entre 0'
            operador = '/'
            temporal = generador.agregarTemporal()
            generador.agregarExpresion(temporal, izq, der, operador)
            self.tipo = Tipos.NUMBER
            return temporal