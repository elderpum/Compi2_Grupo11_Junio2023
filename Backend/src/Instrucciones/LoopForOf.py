from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.Simbolo import Simbolo
from ..Helpers.TiposDatos import Tipos
from datetime import datetime
from ..Instrucciones.BreakC import Break
from ..Instrucciones.ContinueC import Continue
from ..Instrucciones.ReturnC import Return
from ..Expresiones.Identificador import Identificador
from ..Expresiones.Primitivas import Primitivas

class ForOf(Abstracta):
    def __init__(self,iterador,iterando, instrucciones, fila, columna):
        self.iterando = iterando
        self.iterador = iterador
        self.instrucciones = instrucciones
        super().__init__(fila, columna)
    def interpretar(self, arbol, tabla):
        if isinstance(self.iterando, Identificador) :
            nuevaTabla = TablaSimbolos('For',tabla)
            simbolo = tabla.getSimbolo(self.iterando.identificador)
            if simbolo == None: return Error('Sintactico','La variable no esta definida', self.fila, self.columna,datetime.now().date())
            if isinstance(simbolo.getValor(), list) or isinstance(simbolo.getValor(),str):
                asig = self.iterador.interpretar(arbol,nuevaTabla)
                if isinstance(asig,Error): return asig
                ite = nuevaTabla.getSimbolo(self.iterador.identificador)
                haveBreak = False
                for contenido in simbolo.getValor():
                    ite.setValor(contenido)
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
                        break
                    else: 
                        continue
            else:
                return Error('Sintactico','El objeto a iterar debe ser ARRAY | STRING', self.fila, self.columna,datetime.now().date())
        else:
            listado = []
            haveBreak = False
            nuevaTabla = TablaSimbolos('For',tabla)
            if isinstance(self.iterando,list):
                for valor in self.iterando: 
                    if self.iterador.getTipo() == valor.getTipo():
                        valo = valor.interpretar(arbol,tabla)
                        if isinstance(valo,Error):return valo
                        listado.append(valo)
                    elif self.iterador.getTipo() == Tipos.ANY :
                        valo = valor.interpretar(arbol,tabla)
                        if isinstance(valo,Error):return valo
                        listado.append(valo)
                    else:
                        return Error("Semantico",'Tipo de dato no corresponde al valor '+str(self.tipo)+' '+str(valor.getTipo()),self.fila, self.columna,datetime.now().date())
            elif isinstance(self.iterando,Primitivas): 
                if self.iterando.getTipo() == Tipos.STRING:
                    listado = self.iterando.valor
            else:
                return Error("Semantico",'El objeto a iterar debe ser ARRAY | STRING',self.fila, self.columna,datetime.now().date())
            asig = self.iterador.interpretar(arbol,nuevaTabla)
            if isinstance(asig,Error): return asig
            ite = nuevaTabla.getSimbolo(self.iterador.identificador)
            for elemento in listado:
                ite.setValor(elemento)
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
                    break
                else: 
                    continue
        pass
    def traducir(self, arbol, tabla):
        pass