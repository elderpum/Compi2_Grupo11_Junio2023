from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.Simbolo import Simbolo
from ..TablaSimbolos.ObjetoStruct import ObjetoStruct
from ..Helpers.TiposDatos import Tipos
from ..Expresiones.Identificador import Identificador
from datetime import datetime
from ..TablaSimbolos.Traductor import Traductor
from ..Helpers.ReturnCo import ReturnCo

class LlamadaFuncion(Abstracta):

    def __init__(self, nombre, parametros, fila, columna):
        self.nombre = nombre
        self.parametros = parametros
        self.trueLbl = ''
        self.falseLbl = ''
        self.tipo = None
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
        funcion = arbol.getFuncion(self.nombre)
        genAux = Traductor()
        traductor = genAux.obtenerInstancia()
        if funcion !=None:
            traductor.nuevoComentario(f'Llamada a funcion {self.nombre}')
            paramValues= []
            temporales = []
            size = tabla.size
            
            for parametro in self.parametros:
                if isinstance(parametro,LlamadaFuncion):
                    self.guardarTemps(traductor,tabla,temporales)
                    a = parametro.traducir(arbol,tabla)
                    if isinstance(a,Error): return a
                    paramValues.append(a)
                    self.recuperarTemps(traductor,tabla, temporales)
                else:
                    value = parametro.traducir(arbol,tabla)
                    if isinstance(value,Error): return value
                    paramValues.append(value)
                    temporales.append(value.getValue())
            temp = traductor.agregarTemporal()
            traductor.agregarExpresion(temp,'P',size+1,'+')
            aux = 0
            if len(funcion.parametros) == len(paramValues):
                for param in paramValues:
                    if funcion.parametros[aux]['tipo'] == param.getType():
                        aux +=1
                        traductor.setStack(temp, param.getValue())
                        if aux != len(paramValues):
                            traductor.agregarExpresion(temp,temp,1,'+')
                    else:
                        traductor.nuevoComentario('Tipo de parametros no valido, Error')
                        return Error('Semantico','Tipo de parametros no valido',self.fila,self.columna, datetime.now().date())
            traductor.nuevoEntorno(size)
            #self.getFuncion(generator=generador) # Sirve para llamar a una funcion nativa
            traductor.llamarFun(funcion.identificador)
            traductor.getStack(temp,'P')
            traductor.retornarEntorno(size)
            traductor.nuevoComentario(f'Fin de la llamada a la funcion {self.nombre}')
            traductor.agregarEspacio()
            
            if funcion.tipo != Tipos.BOOLEAN:
                return ReturnCo(temp,funcion.tipo, True)
            else:
                traductor.nuevoComentario('Recuperacion de booleano')
                if self.trueLbl == '':
                    self.trueLbl = traductor.nuevaEtiqueta()
                if self.falseLbl == '':
                    self.falseLbl = traductor.nuevaEtiqueta()
                traductor.agregarIf(temp,1,'==',self.trueLbl)
                traductor.agregarGoto(self.falseLbl)
                ret = ReturnCo(temp, funcion.tipo, True)
                ret.trueLbl = self.trueLbl
                ret.falseLbl = self.falseLbl
                traductor.nuevoComentario('Fin de recuperacion de booleano')
                return ret
    
    
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