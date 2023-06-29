from src.Helpers.TiposDatos import Tipos
class ElementoStruct:
    
        
    def __init__(self, identificador,valor):
        self.identificador = identificador
        self.valor = valor
    
    # Getters    
    def getIdentificador(self):
        return self.identificador
    # def getTipo(self):
    #     return self.tipo
    def getValor(self):
        return self.valor
    
    # setters
    def setIdentificador(self, identificador):
        self.identificador = identificador
    # def setTipo(self,tipo):
    #     self.tipo = tipo
    def setValor(self,valor):
        self.valor = valor