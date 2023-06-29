from src.Helpers.TiposDatos import Tipos
class AtributoStruct:
    
        
    def __init__(self, identificador, tipo):
        self.identificador = identificador
        self.tipo = tipo
    
    # Getters    
    def getIdentificador(self):
        return self.identificador
    def getTipo(self):
        return self.tipo
    
    
    # setters
    def setIdentificador(self, identificador):
        self.identificador = identificador
    def setTipo(self,tipo):
        self.tipo = tipo
    