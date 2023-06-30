from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.Error import Error
from .ReturnC import Return
from datetime import datetime
from ..TablaSimbolos.Traductor import Traductor
from ..Helpers.ReturnCo import ReturnCo
from ..Instrucciones.ReturnC import Return

class Funciones(Abstracta):
    def __init__(self,identificador, parametros, instrucciones, tipo ,fila, columna):
        self.identificador = identificador
        self.parametros = parametros
        self.instrucciones = instrucciones
        self.tipo = tipo
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        #entorno = TablaSimbolos(self.identificador,tabla)
        for instruccion in self.instrucciones:
            value = instruccion.interpretar(arbol, tabla)
            if isinstance(value, Error): return value
            if isinstance(value, Return):
                self.tipo = value.tipo
                return value.value
        return None
    def traducir(self, arbol, tabla):
        funcion = arbol.getFuncion()
        if funcion != None: 
            return Error('Semantico', f'Ya existe la funcion {self.identificador}',self.fila,self.columna,datetime.now().date())
        genAux = Traductor()
        traductor = genAux.obtenerInstancia()
        traductor.nuevoComentario(f'Funcion {self.identificador}')
        entorno = TablaSimbolos(self.identificador,tabla)
        Lblreturn = traductor.nuevaEtiqueta()
        entorno.returnLbl = Lblreturn
        entorno.size = 1
        if self.parametros !=None:
            for parametro in self.parametros:
                #if not isinstance(parametro['tipo'], list):
                simbolo = entorno.setTabla(parametro['id'], parametro['tipo'][0], True)    
                simbolo.setTipoAux(parametro['tipo'][1])
        traductor.enFuncion = True
        traductor.agregarInicioF(self.identificador)
        for instruccion in self.instrucciones:
            value = instruccion.traducir(arbol,entorno)
            if isinstance(value, Error):return Error
            if isinstance(value, Return):
                if value.getTrueLbl()=='':
                    traductor.nuevoComentario('Valor a retornar')
                    traductor.setStack('P',value.getValor())
                    traductor.agregarGoto(entorno.returnLbl)
                    traductor.nuevoComentario('Fin Valor a retornar')
                else:
                    traductor.nuevoComentario('Resultado a retornar en la funcion')
                    traductor.colocarEtiqueta(value.getTrueLbl())
                    traductor.setStack('P', '1')
                    traductor.agregarGoto(entorno.returnLbl)
                    traductor.colocarEtiqueta(value.getFalseLbl())
                    traductor.setStack('P', '0')
                    traductor.agregarGoto(entorno.returnLbl)
                    traductor.nuevoComentario('Fin del resultado a retornar')
        traductor.agregarGoto(Lblreturn)
        traductor.colocarEtiqueta(Lblreturn)

        traductor.nuevoComentario(f'Fin de la funcion {self.identificador}')
        traductor.agregarFinF()
        traductor.agregarEspacio()
        traductor.enFuncion = False
        return