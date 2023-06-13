from ..Tabla.Tabla_simbolos import Tabla_Simbolo
from ..Tabla.Arbol import Arbol
from ..Tabla.NodeAST import NodoAST
from abc import ABC, abstractmethod


class Instruccion(ABC):

    def __init__(self, tipo, fila, columna):
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        super().__init__()

    @abstractmethod
    def Ejecutar(self, arbol: Arbol, tabla: Tabla_Simbolo):
        pass

    @abstractmethod
    def getNodo(self) -> NodoAST:
        pass
