from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from datetime import datetime


class Continue(Abstracta):
    def __init__(self, fila, columna):
        super().__init__(fila, columna)
    
    def interpretar(self, arbol, tabla):
        bfor = tabla.getEntorno('For')
        bwhile = tabla.getEntorno('While')
        if bfor != None or bwhile != None:
            return self
            
        else: 
            return Error('Semantico', 'La instruccion Break debe estar en un ciclo',self.fila, self.columna, datetime.now().date())
    def traducir(self, arbol, tabla):
        pass