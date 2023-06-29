from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Simbolo import Simbolo
from ..Helpers.TiposDatos import Tipos
from ..TablaSimbolos.DefStruct import DefinicionStruct
from datetime import datetime

class CreacionInterface(Abstracta):
    def __init__(self, identificador, atributos, fila, columna):
        self.identificador = identificador
        self.atributos = atributos
        self.tipo = Tipos.INTERFACE
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        nuevaEstructura = DefinicionStruct(self.identificador,self.atributos,self.fila, self.columna)
        result = tabla.nuevaEstructura(nuevaEstructura)
        if isinstance(result,Error): return result
    def traducir(self, arbol, tabla):
        pass
        
        
        