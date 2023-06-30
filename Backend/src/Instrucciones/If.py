from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..Helpers.TiposDatos import Tipos
from datetime import datetime
from ..Instrucciones.BreakC import Break
from ..Instrucciones.ReturnC import Return
from ..Instrucciones.ContinueC import Continue
from ..Helpers.ReturnCo import ReturnCo
from ..TablaSimbolos.Traductor import Traductor

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
        genAux = Traductor()
        traductor = genAux.obtenerInstancia()
        traductor.nuevoComentario('Interpretacion If')
        condicion = self.condicion.traducir(arbol, tabla)
        if isinstance(condicion,Error): return condicion
        if condicion.getType() == Tipos.BOOLEAN:
            traductor.nuevaEtiqueta()
            entorno = TablaSimbolos('IF',tabla)
            for instruccion in self.bloqueTrue:
                entorno.breakLbl = tabla.breakLbl
                entorno.continueLbl = tabla.continueLbl
                entorno.returnLbl = tabla.returnLbl
                result = instruccion.traducir(arbol,entorno)
                if isinstance(result,Error):
                    return result
                if isinstance(result,Return):
                    if entorno.returnLbl != '':
                        traductor.nuevoComentario('Retornar en funcion')
                        if result.getTrueLbl()=='':
                            traductor.setStack('P',result.getValor())
                            traductor.agregarGoto(entorno.returnLbl)
                            traductor.nuevoComentario('Fin Retorno Funcion')
                        else:
                            traductor.colocarEtiqueta(result.getTrueLbl())
                            traductor.setStack('P', '1')
                            traductor.agregarGoto(entorno.returnLbl)
                            traductor.colocarEtiqueta(result.getFalseLbl())
                            traductor.setStack('P', '0')
                            traductor.agregarGoto(entorno.returnLbl)
                        traductor.nuevoComentario('Fin del resultado a retornar en la funcion')
            salir = traductor.nuevaEtiqueta()
            traductor.agregarGoto(salir)
            traductor.colocarEtiqueta(condicion.getFalseLbl())
            if self.bloqueFalse != None:
                entorno = TablaSimbolos('ELSE',tabla)  #NUEVO ENTORNO - HIJO - Vacio
                for instruccion in self.bloqueFalse:
                    entorno.breakLbl = tabla.breakLbl
                    entorno.continueLbl = tabla.continueLbl
                    entorno.returnLbl = tabla.returnLbl
                    result = instruccion.traducir(arbol, entorno)
                    if isinstance(result, Error):
                        return result
                    if isinstance(result, Return):
                        traductor.nuevoComentario('Resultado a retornar en la funcion')
                        if result.getTrueLbl() == '':
                            traductor.setStack('P', result.getValor())
                            traductor.agregarGoto(entorno.returnLbl)
                            traductor.nuevoComentario('Fin del resultado a retornar en la funcion')
                        else:
                            traductor.colocarEtiqueta(result.getTrueLbl())
                            traductor.setStack('P', '1')
                            traductor.agregarGoto(entorno.returnLbl)
                            traductor.colocarEtiqueta(result.getFalseLbl())
                            traductor.setStack('P', '0')
                            traductor.agregarGoto(entorno.returnLbl)
                        traductor.nuevoComentario('Fin del resultado a retornar en la funcion')
            traductor.colocarEtiqueta(salir)
        traductor.nuevoComentario('Fin de la compilacion de un if')

