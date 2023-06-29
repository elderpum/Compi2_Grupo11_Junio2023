from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.Simbolo import Simbolo
from ..TablaSimbolos.ObjetoStruct import ObjetoStruct
from ..Helpers.TiposDatos import Tipos
from ..Expresiones.Identificador import Identificador
from datetime import datetime
from ..TablaSimbolos.Traductor import Traductor

class LlamadaFuncion(Abstracta):

    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.trueLbl = ''
        self.falseLbl = ''
        super().__init__(fila, columna)
        
    def getTipo(self):
        return self.tipo
        

    def interpretar(self, arbol, tabla):
        result = arbol.getFuncion(self.nombre)
        
        if result == None:
            return Error("Semantico", "No se encontro la funcion: " + str(self.nombre), str(self.fila), str(self.columna),datetime.now().date())
        entorno = TablaSimbolos(self.nombre,arbol.getTablaGlobal())
        # if len(self.parametros) == len(result.parametros):
        #     # aqui se hace la declaracion de los parametros
        #     pass
        if len(self.parametros) == len(result.parametros):
            contador = 0
            for expresion in self.parametros:
                resultE = expresion.interpretar(arbol, tabla)
                if isinstance(resultE, Error): return resultE
                if result.parametros[contador]['tipo'] == expresion.tipo:
                    #not any(expresion.getTipo() == tipo.name for tipo in Tipos)
                    if any(expresion.getTipo() == tipo.name for tipo in Tipos):
                        objeto = ObjetoStruct(str(result.parametros[contador]['id']),resultE,result.parametros[contador]['tipo'],self.fila, self.columna)
                        resultT = entorno.setFuncion(objeto)
                    else:
                        simbolo = Simbolo(str(result.parametros[contador]['id']), expresion.tipo, resultE,str(entorno.getNombre()), self.fila, self.columna)
                        arbol.getTablaSimbolosGlobalInterpretada()[str(result.parametros[contador]['id'])] = simbolo
                        resultT = entorno.setFuncion(simbolo)
                    if isinstance(resultT, Error): return resultT
                elif result.parametros[contador]['tipo'] == Tipos.ANY or expresion.tipo == Tipos.ANY:
                    simbolo = Simbolo(str(result.parametros[contador]['id']), expresion.tipo, resultE,str(entorno.getNombre()), self.fila, self.columna)
                    resultT = entorno.setFuncion(simbolo)
                    arbol.getTablaSimbolosGlobalInterpretada()[str(result.parametros[contador]['id'])] = simbolo
                    if isinstance(resultT, Error): return resultT
                
                else:
                    return Error("Semantico", "Tipo de dato diferente en Parametros", str(self.fila), str(self.columna),datetime.now().date())
                contador += 1

        value = result.interpretar(arbol, entorno) # me puede retornar un valor

        if isinstance(value, Error): return value
        self.tipo = result.tipo
        return value
    def traducir(self, arbol, tabla):
        pass
    
    
    def guardarTemps(self, generador:Traductor, tabla, tmp2):
        generador.nuevoComentario('Guardando temporales')
        tmp = generador.agregarTemporal()
        for tmp1 in tmp2:
            generador.agregarExpresion(tmp, 'P', tabla.size, '+')
            generador.setStack(tmp, tmp1)
            tabla.size += 1
        generador.nuevoComentario('Fin de guardado de temporales')
    
    def recuperarTemps(self, generador:Traductor, tabla, tmp2):
        generador.nuevoComentario('Recuperando temporales')
        tmp = generador.agregarTemporal()
        for tmp1 in tmp2:
            tabla.size -= 1
            generador.agregarExpresion(tmp, 'P', tabla.size, '+')
            generador.getStack(tmp1, tmp)
        generador.nuevoComentario('Fin de recuperacion de temporales')