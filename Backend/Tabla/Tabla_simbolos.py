from .Simbolo import Simbolo

class TablaSimbolo(object):

    def __init__(self, anterior_=None, Entorno_ = ""):
        self.anterior = anterior_
        self.tabla = {}
        self.Entorno = Entorno_
        self.funcion = False

    def setvariable(self, simbolo: Simbolo):
        entorno = self
        while entorno is not None:
            
            try:
                variable = entorno.getTable()[simbolo.getID()]
            except Exception:
                variable = None

            if variable is not None:
                return False
            else:
                entorno = entorno.getAnterior()
        self.tabla[simbolo.getID()] = simbolo
        return True
    
    def getvariable(self, ID_, funcion_ = False):
        entorno = self
        while entorno is not None:
            try:
                variable = entorno.getTable()[ID_]
            except Exception:
                variable = None

            if variable is not None:
                return variable
            else:
                entorno = entorno.getAnterior()
                    
        return None

    def getTable(self):
        return self.tabla

    def getAnterior(self):
        return self.anterior
