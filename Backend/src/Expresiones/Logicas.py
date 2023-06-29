from ..Abstracta.Abstracta import Abstracta
from ..Helpers.OperacionesLogicas import OperacionL
from ..Helpers.TiposDatos import Tipos
from ..TablaSimbolos.Traductor import Traductor

class Logicas(Abstracta):
    def __init__(self,operadorIzq, operadorDere, operacion, fila, columna):
        self.operadorIzq = operadorIzq
        self.operadorDere = operadorDere
        self.operacion = operacion
        self.tipo = Tipos.BOOLEAN
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
        izq = None if self.operadorIzq == None else self.operadorIzq.interpretar(arbol, tabla)
        tipoIzq = None if self.operadorIzq == None else self.operadorIzq.getTipo()
        dere = self.operadorDere.interpretar(arbol, tabla)
        tipoDere = self.operadorDere.getTipo()
        if self.operacion == OperacionL.AND:
            if tipoIzq == Tipos.BOOLEAN and tipoDere == Tipos.BOOLEAN:
                return izq and dere
            if tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                if isinstance(izq,bool) and isinstance(dere,bool):
                    return izq and dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.BOOLEAN:
                if isinstance(izq,bool):
                    return izq and dere
            elif tipoIzq == Tipos.BOOLEAN and tipoDere == Tipos.ANY:
                if isinstance(dere,bool):
                    return izq and dere
            else:
                return 'Error: Tipos invalidos para operacin Logica'
        elif self.operacion == OperacionL.OR:
            if tipoIzq == Tipos.BOOLEAN and tipoDere == Tipos.BOOLEAN:
                return izq or dere
            if tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                if isinstance(izq,bool) and isinstance(dere,bool):
                    return izq or dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.BOOLEAN:
                if isinstance(izq,bool):
                    return izq or dere
            elif tipoIzq == Tipos.BOOLEAN and tipoDere == Tipos.ANY:
                if isinstance(dere,bool):
                    return izq or dere
            else:
                return 'Error: Tipos invalidos para operacin Logica'
        elif self.operacion == OperacionL.NOT:
            if tipoIzq == None and tipoDere == Tipos.BOOLEAN:
                return not dere
            if tipoIzq == None and tipoDere == Tipos.ANY:
                if isinstance(dere,bool):
                    return not dere
            elif tipoIzq != None:
                return 'Error: Not es operacion Unaria'
            else:
                return 'Error: Tipos invalidos para operacin Logica'
    
    def getTipo(self):
        return self.tipo
    
    def getValor(self, valor, tipo):
        #validar tipo
        return str(valor)
    
    def checkLabels(self):
        genAux = Traductor()
        generador = genAux.obtenerInstancia()
        if self.trueLbl == '':
            self.trueLbl = generador.nuevaEtiqueta()
        if self.falseLbl == '':
            self.falseLbl = generador.nuevaEtiqueta()
    def traducir(self, arbol, tabla):
        tAux = Traductor()
        traductor = tAux.obtenerInstancia()