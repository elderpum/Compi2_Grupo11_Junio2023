from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta 
from ..Helpers.TiposDatos import Tipos
from datetime import datetime

class AccesoAtributo(Abstracta):
    def __init__(self,identificador, atributo, fila, columna):
        self.identificador = identificador 
        self.atributo = atributo
        self.tipo = None
        super().__init__(fila, columna)
        
    def getTipo(self):
        return self.tipo
    def setTipo(self,tipo):
        self.tipo = tipo
    def interpretar(self, arbol, tabla):
        objeto = tabla.getObjeto(self.identificador)
        if objeto == None: return Error('Semantico','No existe el objeto '+ str(self.identificador),self.fila,self.columna,datetime.now().date())
        atributosO = objeto.getAtributos()
        for atributo in atributosO:
            if isinstance(atributo, list) and len(atributo) == 1:
                if atributo.getIdentificador() == self.atributo:
                    if isinstance(atributo.getValor(),str):
                        self.tipo = Tipos.STRING
                    elif isinstance(atributo.getValor(),bool):
                        self.tipo = Tipos.BOOLEAN
                    elif isinstance(atributo.getValor(),int) or isinstance(atributo.getValor(),float):
                        self.tipo = Tipos.NUMBER
                    else:
                        self.tipo = Tipos.ANY
                    return atributo.getValor()
            else:
                # for ide in atributo:
                #     objeto2 = tabla.getObjeto(ide)
                #     if objeto2 == None: return Error('Semantico','No existe el objeto',self.fila,self.columna,datetime.now().date())
                #     atributosO2 = objeto2.getAtributos()
                #     for atributo2 in atributosO2:
                #         if atributo2.getIdentificador() == self.atributo:
                #             if isinstance(atributo.getValor(),str):
                #                 self.tipo = Tipos.STRING
                #             elif isinstance(atributo.getValor(),bool):
                #                 self.tipo = Tipos.BOOLEAN
                #             elif isinstance(atributo.getValor(),int) or isinstance(atributo.getValor(),float):
                #                 self.tipo = Tipos.NUMBER
                #             else:
                #                 self.tipo = Tipos.ANY
                #             return atributo.getValor()
                ide2 = self.atributo[0]
                val = self.atributo[1]
                objeto2 = self.atribObjeto(objeto,ide2)
                if objeto2 == None: return Error('Semantico','No existe el objeto '+str(ide2),self.fila,self.columna,datetime.now().date())
                atributosO2 = objeto2.getValor()
                #for atr in atributosO2:
                if atributosO2.getIdentificador() == ide2:
                    if isinstance(atributo.getValor(),str):
                        self.tipo = Tipos.STRING
                    elif isinstance(atributo.getValor(),bool):
                        self.tipo = Tipos.BOOLEAN
                    elif isinstance(atributo.getValor(),int) or isinstance(atributo.getValor(),float):
                        self.tipo = Tipos.NUMBER
                    else:
                        self.tipo = Tipos.ANY
                    return atributo.getValor()
        return Error('Semantico','El atributo no existe '+str(ide2),self.fila,self.columna,datetime.now().date())
    
    def atribObjeto(self,objeto, identificador):
        for obj in objeto.getAtributos():
            if obj.identificador == identificador:
                return obj
        return None
    def traducir(self, arbol, tabla):
        pass