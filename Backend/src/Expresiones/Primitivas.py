from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Traductor import Traductor
from ..Helpers.TiposDatos import Tipos
from ..Helpers.ReturnCo import ReturnCo

class Primitivas(Abstracta):
    def __init__(self,tipo,valor, fila, columna):
        self.tipo = tipo
        self.valor  = valor
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
        return self.valor
    
    def getTipo(self):
        return self.tipo
    def getValor(self):
        return self.valor
    def traducir(self, arbol, tabla):
        genAux = Traductor()
        traductor = genAux.obtenerInstancia()
        if self.tipo == Tipos.NUMBER:
            return ReturnCo(str(self.valor),self.tipo,False)
        elif self.tipo == Tipos.STRING:
            temporal = traductor.agregarTemporal()
            traductor.agregarAsignacion(temporal, 'H')
            for caracter in str(self.valor):
                traductor.setHeap('H',ord(caracter))
                traductor.siguienteHeap()
            traductor.setHeap('H',-1)
            traductor.siguienteHeap()
            
            return ReturnCo(temporal, self.tipo, True)
        elif self.tipo == Tipos.BOOLEAN:
            if self.trueLbl == '':
                self.trueLbl = traductor.nuevaEtiqueta()
            if self.falseLbl == '':
                self.falseLbl = traductor.nuevaEtiqueta()
            
            if self.valor:
                traductor.agregarGoto(self.trueLbl)
                traductor.nuevoComentario('GOTO')
                traductor.agregarGoto(self.falseLbl)
            else: 
                traductor.agregarGoto(self.falseLbl)
                traductor.nuevoComentario('GOTO')
                traductor.agregarGoto(self.trueLbl)
            ret = ReturnCo(self.valor, self.tipo, False)
            ret.setTrueLbl(self.trueLbl)
            ret.setFalseLbl(self.falseLbl)
            return ret