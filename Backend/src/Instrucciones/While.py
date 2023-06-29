from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.Simbolo import Simbolo
from ..Helpers.TiposDatos import Tipos
from datetime import datetime
from .BreakC import Break
from .ContinueC import Continue
from .ReturnC import Return

class While(Abstracta):
    def __init__(self, condicion, instrucciones, fila, columna):
        self.condicion = condicion
        self.instrucciones = instrucciones
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        nuevaTabla = TablaSimbolos('While',tabla)
        
        condicion = self.condicion.interpretar(arbol, nuevaTabla)
        if isinstance(condicion, Error): return condicion # manejar error
        
        if self.condicion.tipo != Tipos.BOOLEAN:
            return Error("Semantico", "Tipo de dato no booleano en FOR.", self.fila, self.columna) #agregar a lista
        haveBreak = False
        while condicion:
            for instruccion in self.instrucciones:
                result = instruccion.interpretar(arbol, nuevaTabla)
                if isinstance(result,Error):
                    arbol.errores.append(result)
                if isinstance(result, Return): return result
                if isinstance(result, Break):
                    haveBreak = True
                    break
                if isinstance(result,Continue): 
                    #por cada instruccion
                    haveBreak = False
                    break
            if haveBreak == True:
                condicion = False
                break
            else:
                condicion = self.condicion.interpretar(arbol, nuevaTabla)


        return None
    def traducir(self, arbol, tabla):
        pass