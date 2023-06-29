from ..Abstracta.Abstracta import Abstracta

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
        pass