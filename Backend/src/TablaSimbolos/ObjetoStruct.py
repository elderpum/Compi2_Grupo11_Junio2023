from .ElementoStruct import ElementoStruct

class ObjetoStruct:
    def __init__(self,identificador,atributos,tipo, fila, columna):
        self.identificador = identificador
        self.atributos = atributos
        self.fila = fila
        self.columna = columna
        self.tipo = tipo
        
    def getTipo(self):
        return self.tipo
    def setTipo(self,tipo):
        self.tipo = tipo
    def getFila(self):
        return self.fila
    def getColumna(self):
        return self.columna
    def getIdentificador(self):
        return self.identificador
    def getAtributos(self):
        return self.atributos
    def setIdentificador(self,identificador):
        self.identificador = identificador
    def setAtributos(self,atributos):
        self.atributos = atributos