from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.ElementoStruct import ElementoStruct
from ..Expresiones.Identificador import Identificador

class Return(Abstracta):

    def __init__(self,expresion, fila, columna):
        self.expresion = expresion
        self.value = None
        self.tipo = None
        super().__init__(fila, columna)

    def interpretar(self, arbol, tabla):
        if isinstance(self.expresion,list):
            expresiones = []
            for exp in self.expresion:
                if isinstance(exp,ElementoStruct):
                    #for exprt in exp.getValor():
                    if isinstance(exp.getValor(),Identificador):
                        result = exp.getValor().interpretar(arbol,tabla)
                        if isinstance(result, Error): return result
                        expresiones.append(exp)
                        self.tipo = exp.getValor().tipo
                    else: 
                        result = exp.getValor().interpretar(arbol,tabla)
                        if isinstance(result, Error): return result
                        expresiones.append(exp)
                        self.tipo = exp.getValor().tipo
            self.value = expresiones
        else:
            result = self.expresion.interpretar(arbol, tabla)
            if isinstance(result, Error): return result
            self.tipo = self.expresion.tipo
            self.value = result
        return self
    def traducir(self, arbol, tabla):
        pass