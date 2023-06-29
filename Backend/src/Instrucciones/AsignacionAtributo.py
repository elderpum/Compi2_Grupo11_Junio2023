from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.Error import Error
from ..Helpers.TiposDatos import Tipos
from datetime import datetime

class AsignacionAtributo(Abstracta):
    def __init__(self,identificador,atributo,valor, fila, columna):
        self.identificador = identificador
        self.atributo = atributo
        self.valor = valor
        super().__init__(fila, columna)

    def interpretar(self, arbol, tabla):
        objeto = tabla.getObjeto(self.identificador)
        if objeto == None: return Error('Semantico','No existe el objeto '+str(self.identificador),self.fila,self.columna,datetime.now().date())
        plantilla = tabla.obtenerEstructura(objeto.getTipo())
        if plantilla == None: return Error('Semantico','No existe el struct definido',self.fila,self.columna, datetime.now().date())
        nuevoValor = self.valor.interpretar(arbol,tabla)
        atributosBase = plantilla.getAtributos()
        if isinstance(nuevoValor,Error): return nuevoValor
        atributosO = objeto.getAtributos()
        ptl = self.existeAtributo(atributosBase,self.atributo)
        if ptl is not None:
            if self.valor.getTipo() == Tipos.ANY:
                upd = self.actualizarValor(self.atributo,nuevoValor,objeto)
                if upd == None:return Error('Semantico', 'No fue posible actualizar el atributo',self.fila,self.columna,datetime.now().date())
                resuslt = tabla.actualizarObjeto(upd)
                if isinstance(resuslt,Error): return resuslt
                return None
                
            elif ptl.getTipo() == self.valor.getTipo():
                upd = self.actualizarValor(self.atributo,nuevoValor,objeto)
                if upd == None:return Error('Semantico', 'No fue posible actualizar el atributo',self.fila,self.columna,datetime.now().date())
                resuslt = tabla.actualizarObjeto(upd)
                if isinstance(resuslt,Error): return resuslt
                return None
        else:
            Error('Semantico','El atributo no esta definido en la estructura',self.fila,self.columna, datetime.now().date())
        
    def existeAtributo(self,plantillaA,id):
        for atr in plantillaA:
            if atr.getIdentificador() == id:
                return atr
        return None
    def obtenerAtributoObjeto(self, atributos, id):
        for atr in atributos:
            if atr.getIdentificador() == id:
                return atr
        return None
    def actualizarValor(self,id,valor,objeto):
        for atr in objeto.getAtributos():
            if atr.getIdentificador() == id:
                atr.setValor(valor)
                return objeto
        return None
    def traducir(self, arbol, tabla):
        pass