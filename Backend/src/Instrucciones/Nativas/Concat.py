from ...Abstracta.Abstracta import Abstracta
from ...TablaSimbolos.TablaSimbolos import TablaSimbolos
from ...TablaSimbolos.Error import Error
from ...Helpers.TiposDatos import Tipos
from ...Expresiones.Primitivas import Primitivas
from datetime import datetime

class Concat(Abstracta):
    def __init__(self, identificador,array ,fila, columna):
        self.identificador = identificador
        self.array = array
        self.tipo = Tipos.STRING #cambiar a array despues
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        simbolo = tabla.getSimbolo(self.identificador)
        if simbolo == None: return Error('Sintactico','La variable no esta definida', self.fila, self.columna,datetime.now().date())
        if isinstance(simbolo.getValor(), list):
            listado = []
            for valor in self.array: 
                if simbolo.getTipo()== valor.getTipo():
                    valo = valor.interpretar(arbol,tabla)
                    if isinstance(valo,Error):return valo
                    listado.append(valo)
                elif simbolo.getTipo() == Tipos.ANY :
                    valo = valor.interpretar(arbol,tabla)
                    if isinstance(valo,Error):return valo
                    listado.append(valo)
                else:
                    return Error("Semantico",'Tipo de dato no corresponde al valor '+str(self.tipo)+' '+str(valor.getTipo()),self.fila, self.columna,datetime.now().date())
            simbolo.getValor().extend(listado)
            tabla.actualizarSimbolo(simbolo)
            self.tipo = simbolo.getTipo()
            return simbolo.getValor()
        else: 
            return Error('Semantico', 'El identificador debe ser STRING',self.fila, self.columna, datetime.now().date())
    def getTipo(self):
        return self.tipo
    def traducir(self, arbol, tabla):
        pass