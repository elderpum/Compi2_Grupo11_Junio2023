
from Tabla.Tabla_simbolos import TablaSimbolo
from Tabla.Arbol import Arbol
from Tabla.NodeAST import NodeAST
from abc import ABC, abstractmethod


class Instruccion(ABC):

    def __init__(self, tipo, fila, columna):
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        super().__init__()

    @abstractmethod
    def Ejecutar(self, arbol_: Arbol, tabla_: TablaSimbolo):
        pass

    @abstractmethod
    def getNodo(self) -> NodeAST:
        pass
