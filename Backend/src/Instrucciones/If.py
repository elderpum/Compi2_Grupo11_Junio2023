from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..Helpers.TiposDatos import Tipos
from datetime import datetime
from ..Instrucciones.BreakC import Break
from ..Instrucciones.ReturnC import Return
from ..Instrucciones.ContinueC import Continue

class If(Abstracta):
    def __init__(self,condicion,bloqueTrue,bloqueFalse, fila, columna):
        self.condicion = condicion
        self.bloqueTrue = bloqueTrue
        self.bloqueFalse = bloqueFalse
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        condicion = self.condicion.interpretar(arbol, tabla)
        if isinstance(condicion, Error):return condicion #manejar error
        if self.bloqueTrue!= None:#si la condicion es verdadera
            if condicion :
                entorno = TablaSimbolos('IF',tabla)
                for instruccion in self.bloqueTrue:
                    result = instruccion.interpretar(arbol,entorno)
                    if isinstance(result, Error): arbol.setErrores(result)
                    if isinstance(result,Return): return result
                    if isinstance(result, Break):return result
                    if isinstance(result, Continue):return result
            
            else:
                if self.bloqueFalse!=None:#si la condicion es falsa
                    entorno = TablaSimbolos('ELSE',tabla)
                    for instruccion in self.bloqueFalse:
                        result = instruccion.interpretar(arbol,entorno)
                        if isinstance(result, Error): arbol.setErrores(result)
                        if isinstance(result,Return): return result
                        if isinstance(result, Break):return result
                        if isinstance(result, Continue):return result
            
        # if self.bloqueFalse!=None:#si la condicion es falsa
        #     if bool(condicion) == False:
        #         entorno = TablaSimbolos(tabla)
        #         for instruccion in self.bloqueTrue:
        #             result = instruccion.interpretar(arbol,entorno)
        #             if isinstance(result, Error): arbol.setErrores(result)
        
    def traducir(self, arbol, tabla):
        pass
