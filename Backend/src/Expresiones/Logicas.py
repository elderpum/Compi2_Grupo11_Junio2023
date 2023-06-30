from ..Abstracta.Abstracta import Abstracta
from ..Helpers.OperacionesLogicas import OperacionL
from ..Helpers.TiposDatos import Tipos
from ..Helpers.ReturnCo import ReturnCo
from ..TablaSimbolos.Traductor import Traductor
from ..TablaSimbolos.Error import Error

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
        traductor.nuevoComentario("Compilacion de Expresion Logica")
        self.checkLabels()
        lblAndOr = ''
        if self.operacion == OperacionL.AND:
            lblAndOr = traductor.nuevaEtiqueta()
            
            self.operadorIzq.setTrueLbl(lblAndOr)
            self.operadorDere.setTrueLbl(self.trueLbl)
            self.operadorIzq.falseLbl = self.operadorDere.falseLbl = self.falseLbl
        elif self.operacion == OperacionL.OR:
            self.operadorIzq.setTrueLbl(self.trueLbl)
            self.operadorDere.setTrueLbl(self.trueLbl)
            lblAndOr = traductor.nuevaEtiqueta()
            
            self.operadorIzq.setFalseLbl(lblAndOr)
            self.operadorDere.setFalseLbl(self.falseLbl)
        elif self.operacion == OperacionL.NOT:
            self.operadorDere.setFalseLbl(self.trueLbl)
            self.operadorDere.setTrueLbl(self.falseLbl)
            lblNot = self.operadorDere.traducir(arbol,tabla)
            if isinstance(lblNot,Error): return lblNot
            lbltrue = lblNot.getTrueLbl()
            lblfalse = lblNot.getFalseLbl()
            lblNot.setTrueLbl(lblfalse)
            lblNot.setFalseLbl(lbltrue)
            self.tipo = Tipos.BOOLEAN
            return lblNot
        izq = self.operadorIzq.traducir(arbol,tabla)
        if isinstance(izq, Error): return izq
        traductor.colocarEtiqueta(lblAndOr)
        dere = self.operadorDere.traducir(arbol,tabla)
        if isinstance(dere,Error): return dere
        traductor.nuevoComentario('Fin expresion logica')
        traductor.agregarEspacio()
        ret = ReturnCo(None, Tipos.BOOLEAN, False)
        ret.setTrueLbl(self.trueLbl)
        ret.setFalseLbl(self.falseLbl)
        return ret


    def checkLabels(self):
        genAux = Traductor()
        generador = genAux.obtenerInstancia()
        if self.trueLbl == '':
            self.trueLbl = generador.nuevaEtiqueta()
        if self.falseLbl == '':
            self.falseLbl = generador.nuevaEtiqueta()
            
    # def getOperador(self):
    #     if self.operacion == OperacionR.IGUALDAD:
    #         return '=='
    #     if self.operacion == OperacionR.DIFERENTE:
    #         return '!='
    #     if self.operacion == OperacionR.MAYOR:
    #         return '>'
    #     if self.operacion == OperacionR.MENOR:
    #         return '<'
    #     if self.operacion == OperacionR.MAYORI:
    #         return '>='
    #     if self.operacion == OperacionR.MAYORI:
    #         return '<='
        