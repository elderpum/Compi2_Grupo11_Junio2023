from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Simbolo import Simbolo
from ..Helpers.TiposDatos import Tipos
from datetime import datetime

class DeclaracionArreglo(Abstracta):
    def __init__(self, identificador, tipo, valores, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.valores = valores
        self.array = Tipos.ARRAY
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        valo = None
        listado = []
        for valor in self.valores: 
            if isinstance(valor,list) and len(valor)>1:
                listadoi = []
                for valor2 in valor:
                    if self.tipo == valor2.getTipo():
                        valo = valor2.interpretar(arbol,tabla)
                        if isinstance(valo,Error):return valo
                        listadoi.append(valo)
                    elif self.tipo == Tipos.ANY :
                        valo = valor2.interpretar(arbol,tabla)
                        if isinstance(valo,Error):return valo
                        listadoi.append(valo)
                    else:
                        return Error("Semantico",'Tipo de dato no corresponde al valor '+str(self.tipo)+' '+str(valor.getTipo()),self.fila, self.columna,datetime.now().date())
                listado.append(listadoi)
            else:
                if self.tipo == valor.getTipo():
                    valo = valor.interpretar(arbol,tabla)
                    if isinstance(valo,Error):return valo
                    listado.append(valo)
                elif self.tipo == Tipos.ANY :
                    valo = valor.interpretar(arbol,tabla)
                    if isinstance(valo,Error):return valo
                    listado.append(valo)
                else:
                    return Error("Semantico",'Tipo de dato no corresponde al valor '+str(self.tipo)+' '+str(valor.getTipo()),self.fila, self.columna,datetime.now().date())
        simbolo = Simbolo(str(self.identificador),self.tipo, listado,str(tabla.getNombre()),self.fila, self.columna)
        arbol.getTablaSimbolosGlobalInterpretada()[self.identificador] = simbolo
        result = tabla.setSimboloTabla(simbolo)
        if isinstance(result,Error):return result
        return None
    def traducir(self, arbol, tabla):
        pass

