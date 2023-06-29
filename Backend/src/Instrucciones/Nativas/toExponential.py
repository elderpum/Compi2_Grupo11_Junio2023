from ...Abstracta.Abstracta import Abstracta
from ...TablaSimbolos.TablaSimbolos import TablaSimbolos
from ...TablaSimbolos.Error import Error
from ...Helpers.TiposDatos import Tipos
from ...Expresiones.Identificador import Identificador
from ...Expresiones.Primitivas import Primitivas
from datetime import datetime

class toExponential(Abstracta):
    def __init__(self,numero, exponente, fila, columna):
        self.numero = numero
        self.exponente = exponente
        self.tipo = Tipos.STRING
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
            simbolo = tabla.getSimbolo(self.numero)
            if simbolo == None: return Error('Sintactico','La variable no esta definida', self.fila, self.columna,datetime.now().date())
            #valor = self.numero.interpretar(arbol,tabla)
            if isinstance(simbolo.getValor(), int) or isinstance(simbolo.getValor(),float):
                exponente = self.exponente.interpretar(arbol,tabla)
                if isinstance(exponente, Error): return exponente
                if self.exponente.getTipo() == Tipos.NUMBER and self.exponente.getTipo() != Tipos.BOOLEAN:
                    #cadena_formateada = "{:.2e{}}".format(simbolo.getValor(), exponente)
                    cadena_formateada = "{:.0f}e{}".format(float(simbolo.getValor() / (10 ** exponente)), exponente)
                    partes = cadena_formateada.split("e")
                    resultado = "{:.2f}+{}".format(float(partes[0]), int(partes[1]))
                    return resultado #Primitivas(Tipos.ANY,resultado,self.fila, self.columna)
                elif self.exponente.getTipo() == Tipos.ANY:
                    if isinstance(exponente,int) or isinstance(exponente,float):
                        cadena_formateada = "{:.0f}e{}".format(float(simbolo.getValor() / (10 ** exponente)), exponente)
                        partes = cadena_formateada.split("e")
                        resultado = "{:.2f}+{}".format(float(partes[0]), int(partes[1]))
                        return resultado #Primitivas(Tipos.ANY,resultado,self.fila, self.columna)
                else:
                    return Error('Semantico', 'El exponente debe ser numerico',self.fila, self.columna, datetime.now().date())
            else: 
                return Error('Semantico', 'La base debe ser numerica',self.fila, self.columna, datetime.now().date())
    def getTipo(self):
        return self.tipo
    def traducir(self, arbol, tabla):
        pass