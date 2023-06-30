from ..Abstracta.Abstracta import Abstracta
from ..Helpers.OperacionesRelacionales import OperacionR
from ..Helpers.TiposDatos import Tipos
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.Traductor import Traductor
from ..Helpers.ReturnCo import ReturnCo

class Relacionales(Abstracta):
    
    def __init__(self, operadorIzq, operadorDere, operacion, fila, columna):
        self.operadorDere = operadorDere
        self.operadorIzq = operadorIzq
        self.operacion = operacion
        self.tipo= Tipos.BOOLEAN
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
        izq = self.operadorIzq.interpretar(arbol, tabla)
        if isinstance(izq, Error): return izq
        tipoIzq = self.operadorIzq.getTipo()
        dere = self.operadorDere.interpretar(arbol, tabla)
        if isinstance(dere, Error): return dere
        tipoDere = self.operadorDere.getTipo()
        if self.operacion == OperacionR.MAYOR:
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                return izq > dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.STRING:
                return izq > dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                if (isinstance(izq,int) or isinstance(izq,float)) and (isinstance(dere,int) or isinstance(dere,float)):
                    return izq > dere
                elif isinstance(izq,str) and isinstance(dere,str):
                    return izq > dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return izq > dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return izq > dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.STRING:
                if (isinstance(izq,str) ):
                    return izq > dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.ANY:
                if (isinstance(dere,str) ):
                    return izq > dere
            else:
                return 'Error: Tipos invalidos para la operacion' #manejar error
        if self.operacion == OperacionR.MENOR:
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                return izq < dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.STRING:
                return izq < dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                if (isinstance(izq,int) or isinstance(izq,float)) and (isinstance(dere,int) or isinstance(dere,float)):
                    return izq < dere
                elif isinstance(izq,str) and isinstance(dere,str):
                    return izq < dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return izq < dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return izq < dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.STRING:
                if (isinstance(izq,str) ):
                    return izq < dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.ANY:
                if (isinstance(dere,str) ):
                    return izq < dere
            else:
                return 'Error: Tipos invalidos para la operacion' #manejar error
        if self.operacion == OperacionR.MAYORI:
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                return izq >= dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.STRING:
                return izq >= dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                if (isinstance(izq,int) or isinstance(izq,float)) and (isinstance(dere,int) or isinstance(dere,float)):
                    return izq >= dere
                elif isinstance(izq,str) and isinstance(dere,str):
                    return izq >= dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return izq >= dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return izq >= dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.STRING:
                if (isinstance(izq,str) ):
                    return izq >= dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.ANY:
                if (isinstance(dere,str) ):
                    return izq >= dere
            else:
                return 'Error: Tipos invalidos para la operacion' #manejar error
        if self.operacion == OperacionR.MENORI:
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                return izq <= dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.STRING:
                return izq <= dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                if (isinstance(izq,int) or isinstance(izq,float)) and (isinstance(dere,int) or isinstance(dere,float)):
                    return izq <= dere
                elif isinstance(izq,str) and isinstance(dere,str):
                    return izq <= dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return izq <= dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return izq <= dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.STRING:
                if (isinstance(izq,str) ):
                    return izq <= dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.ANY:
                if (isinstance(dere,str) ):
                    return izq <= dere
            else:
                return 'Error: Tipos invalidos para la operacion' #manejar error
        if self.operacion == OperacionR.IGUALDAD:
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                return izq == dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.STRING:
                return izq == dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                if (isinstance(izq,int) or isinstance(izq,float)) and (isinstance(dere,int) or isinstance(dere,float)):
                    return izq == dere
                elif isinstance(izq,str) and isinstance(dere,str):
                    return izq == dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return izq == dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return izq == dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.STRING:
                if (isinstance(izq,str) ):
                    return izq == dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.ANY:
                if (isinstance(dere,str) ):
                    return izq == dere
            else:
                return 'Error: Tipos invalidos para la operacion' #manejar error
        if self.operacion == OperacionR.DIFERENTE:
            if tipoIzq == Tipos.NUMBER and tipoDere == Tipos.NUMBER:
                return izq != dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.STRING:
                return izq != dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.ANY:
                if (isinstance(izq,int) or isinstance(izq,float)) and (isinstance(dere,int) or isinstance(dere,float)):
                    return izq != dere
                elif isinstance(izq,str) and isinstance(dere,str):
                    return izq != dere
            elif tipoIzq == Tipos.NUMBER and tipoDere == Tipos.ANY:
                if (isinstance(dere,int) or isinstance(dere,float)):
                    return izq != dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.NUMBER:
                if (isinstance(izq,int) or isinstance(izq,float)):
                    return izq != dere
            elif tipoIzq == Tipos.ANY and tipoDere == Tipos.STRING:
                if (isinstance(izq,str) ):
                    return izq != dere
            elif tipoIzq == Tipos.STRING and tipoDere == Tipos.ANY:
                if (isinstance(dere,str) ):
                    return izq != dere
            else:
                return 'Error: Tipos invalidos para la operacion' #manejar error
            
            
    def getTipo(self):
        return self.tipo
    
    def getValor(self,valor,tipo):
        #validar tipo
        return str(valor)
    def traducir(self, arbol, tabla):
        genAux = Traductor()
        generador = genAux.obtenerInstancia()
        generador.nuevoComentario("Traduccion de Expresion Relacional")
        izq = self.operadorIzq.traducir(arbol,tabla)
        if isinstance(izq,Error): return izq
        dere = None
        result = ReturnCo(None,Tipos.BOOLEAN,False)
        
        if izq.getType() != Tipos.BOOLEAN:
            dere = self.operadorDere.traducir(arbol,tabla)
            if isinstance(dere,Error): return dere
            if (izq.getType() == Tipos.NUMBER) and (dere.getType() == Tipos.NUMBER):
                self.checkLabels()
                generador.agregarIf(izq.getValue(),dere.getValue(),self.getOperador(),self.getTrueLbl())
                generador.agregarGoto(self.getFalseLbl())
            elif (izq.getType() == Tipos.STRING) and (dere.getType() == Tipos.STRING):
                if self.operacion == OperacionR.IGUALDAD or self.operacion == OperacionR.DIFERENTE:
                    generador.fcompareString()
                    paramTemp = generador.agregarTemporal()
                    generador.agregarExpresion(paramTemp, 'P',tabla.size, '+')
                    generador.agregarExpresion(paramTemp, paramTemp,'1', '+')
                    generador.setStack(paramTemp,izq.getValue())
                    
                    generador.agregarExpresion(paramTemp, paramTemp,'1', '+')
                    generador.setStack(paramTemp,dere.getValue())
                    
                    generador.nuevoEntorno(tabla.size)
                    generador.llamarFun('compareString')
                    temp = generador.agregarTemporal()
                    
                    generador.getStack(temp,'P')
                    generador.retornarEntorno(tabla.size)
                    self.checkLabels()
                    
                    generador.agregarIf(temp,self.getNum(), '==' ,self.trueLbl)
                    generador.agregarGoto(self.falseLbl)
                    result.setTrueLbl(self.trueLbl)
                    result.setFalseLbl(self.falseLbl)
                    return result
        generador.nuevoComentario("Fin de compilacion de Expresion Relacional")
        generador.agregarEspacio()
        result.setTrueLbl(self.trueLbl)
        result.setFalseLbl(self.falseLbl)
        return result
                    
                
    def getNum(self):
        if self.operacion == OperacionR.IGUALDAD:
            return '1'
        if self.operacion == OperacionR.DIFERENTE:
            return '0'
    def checkLabels(self):
        genAux = Traductor()
        generador = genAux.obtenerInstancia()
        if self.trueLbl == '':
            self.trueLbl = generador.nuevaEtiqueta()
        if self.falseLbl == '':
            self.falseLbl = generador.nuevaEtiqueta()
            
    def getOperador(self):
        if self.operacion == OperacionR.IGUALDAD:
            return '=='
        if self.operacion == OperacionR.DIFERENTE:
            return '!='
        if self.operacion == OperacionR.MAYOR:
            return '>'
        if self.operacion == OperacionR.MENOR:
            return '<'
        if self.operacion == OperacionR.MAYORI:
            return '>='
        if self.operacion == OperacionR.MENORI:
            return '<='
        