from .Tipo import Tipos


class Simbolo(object):
    def __init__(self, valor_, tipo_: Tipos, id_, fila_, columna_):
        self.tipo = tipo_
        self.id = id_
        self.fila = fila_
        self.columna = columna_
        self.valor = valor_
        
    def getID(self):
        return self.id

    def getTipo(self):
        return self.tipo

    def getTipoRango(self):
        return self.tipado_rango
    
    def getValor(self):
        return self.valor
    
    def setValor(self, valor_):
        self.valor = valor_

    def setTipoRango(self, tipo_:Tipos):
        self.tipado_rango = tipo_

    def setTipo(self, tipo_: Tipos):
        self.tipo = tipo_

 

   