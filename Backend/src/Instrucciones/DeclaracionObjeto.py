from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Simbolo import Simbolo
from ..Helpers.TiposDatos import Tipos
from ..TablaSimbolos.ObjetoStruct import ObjetoStruct
from ..TablaSimbolos.AtributoS import AtributoStruct
from ..TablaSimbolos.ElementoStruct import ElementoStruct
from ..TablaSimbolos.DefStruct import DefinicionStruct
from datetime import datetime

class DeclaracionObjeto(Abstracta):
    def __init__(self,identificador,struct,atributos, fila, columna):
        self.identificador = identificador
        self.struct = struct
        self.atributos = atributos
        self.tipo = Tipos.INTERFACE
        super().__init__(fila, columna)
    def interpretar(self, arbol, tabla):
        plantilla = tabla.obtenerEstructura(self.struct)
        if plantilla == None: return Error('Semantico','No existe el struct definido',self.fila,self.columna, datetime.now().date())
        nuevosValores = self.atributos
        atributosBase = plantilla.getAtributos()
        # if atributosBase != None and isinstance(atributosBase[0],AtributoStruct):
        #     pass
        
        for indice in range(0,len(nuevosValores)):
            ptl = self.existeAtributo(atributosBase,nuevosValores[indice].getIdentificador())
            if ptl is not None:
                if isinstance(ptl, AtributoStruct):
                    ptl.getTipo()
                    plantillaI = tabla.obtenerEstructura(ptl.getTipo())
                    if plantillaI == None: return Error('Semantico','No existe el struct definido',self.fila,self.columna, datetime.now().date())
                    nuevosValoresI = nuevosValores[indice].getValor()
                    atributosBaseI = plantillaI.getAtributos()
                    for ind in range(0,len(nuevosValoresI)):
                        ptli = self.existeAtributo(atributosBaseI,nuevosValoresI[ind].getIdentificador())
                        if ptli is not None:
                            if ptli.getTipo() == Tipos.STRING:
                                valori = nuevosValoresI[ind].getValor().interpretar(arbol,tabla)
                                if isinstance(valori,str):
                                #nuevosValores[indice].getTipo() == ptl.getTipo():
                                    #nuevosValoresI[ind].setValor(valori)
                                    pass
                            elif ptli.getTipo() == Tipos.NUMBER:
                                valori = nuevosValoresI[ind].getValor().interpretar(arbol,tabla)
                                if isinstance(valori,int) or isinstance(valori,float):
                                #nuevosValores[indice].getTipo() == ptl.getTipo():
                                    pass
                                    #nuevosValoresI[ind].setValor(valori)
                            elif ptli.getTipo() == Tipos.BOOLEAN:
                                valori = nuevosValoresI[ind].getValor().interpretar(arbol,tabla)
                                if isinstance(valori,bool):
                                #nuevosValores[indice].getTipo() == ptl.getTipo():
                                    #nuevosValoresI[ind].setValor(valori)
                                    pass
                            elif ptli.getTipo() == Tipos.ANY:
                                valori = nuevosValoresI[ind].getValor().interpretar(arbol,tabla)
                                #nuevosValores[indice].getTipo() == ptl.getTipo():
                                #nuevosValoresI[ind].setValor(valori)
                            else:
                                Error('Semantico','El tipo de dato no coincide, debe ser '+str(ptli.getTipo()),self.fila,self.columna, datetime.now().date())
                    # nuevoObjetoI = ElementoStruct(nuevosValoresI[ind].getIdentificador(),nuevosValoresI[ind].getValor())
                    # nuevosValores[indice].setValor(nuevoObjetoI)
                elif ptl.getTipo() == Tipos.STRING:
                    valor = nuevosValores[indice].getValor().interpretar(arbol,tabla)
                    if isinstance(valor,str):
                    #nuevosValores[indice].getTipo() == ptl.getTipo():
                        nuevosValores[indice].setValor(valor)
                elif ptl.getTipo() == Tipos.NUMBER:
                    valor = nuevosValores[indice].getValor().interpretar(arbol,tabla)
                    if isinstance(valor,int) or isinstance(valor,float):
                    #nuevosValores[indice].getTipo() == ptl.getTipo():
                        nuevosValores[indice].setValor(valor)
                elif ptl.getTipo() == Tipos.BOOLEAN:
                    valor = nuevosValores[indice].getValor().interpretar(arbol,tabla)
                    if isinstance(valor,bool):
                    #nuevosValores[indice].getTipo() == ptl.getTipo():
                        nuevosValores[indice].setValor(valor)
                elif ptl.getTipo() == Tipos.ANY:
                    valor = nuevosValores[indice].getValor().interpretar(arbol,tabla)
                    #nuevosValores[indice].getTipo() == ptl.getTipo():
                    nuevosValores[indice].setValor(valor)
                else:
                    Error('Semantico','El tipo de dato no coincide, debe ser '+str(ptl.getTipo()),self.fila,self.columna, datetime.now().date())
            else:
                Error('Semantico','El atributo no esta definido en la estructura',self.fila,self.columna, datetime.now().date())
        nuevoObjeto = ObjetoStruct(self.identificador,self.atributos,self.struct,self.fila,self.columna)
        rt = tabla.nuevoObjeto(nuevoObjeto)
        if isinstance(rt,Error):return rt
        return None
    def existeAtributo(self,plantillaA,id):
        for atr in plantillaA:
            if atr.getIdentificador() == id:
                return atr
        return None
    def traducir(self, arbol, tabla):
        pass
    