from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Error import Error
from ..TablaSimbolos.TablaSimbolos import TablaSimbolos
from ..TablaSimbolos.Simbolo import Simbolo
from ..Helpers.TiposDatos import Tipos
from datetime import datetime
from ..Instrucciones.BreakC import Break
from ..Instrucciones.ContinueC import Continue
from ..Instrucciones.ReturnC import Return
from ..TablaSimbolos.Traductor import Traductor
from ..Helpers.ReturnCo import ReturnCo

class LoopFor(Abstracta):
    def __init__(self,inicio, condicion, incremento, instrucciones, fila, columna):
        self.inicio = inicio
        self.condicion = condicion
        self.incremento = incremento
        self.instrucciones = instrucciones
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
        nuevaTabla = TablaSimbolos('For',tabla)
        inicio = self.inicio.interpretar(arbol, nuevaTabla)
        if isinstance(inicio, Error): return inicio
        
        condicion = self.condicion.interpretar(arbol, nuevaTabla)
        if isinstance(condicion, Error): return condicion # manejar error
        
        if self.condicion.tipo != Tipos.BOOLEAN:
            return Error("Semantico", "Tipo de dato no booleano en FOR.", self.fila, self.columna) #agregar a lista
        haveBreak = False
        while condicion:
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
            if haveBreak == False:
                nuevoValor = self.incremento.interpretar(arbol, nuevaTabla)
                if isinstance(nuevoValor, Error): return nuevoValor
                simbolo = Simbolo(self.inicio.identificador, self.inicio.tipo, nuevoValor,str(nuevaTabla.getNombre()),self.fila,self.columna)
                
                valor = nuevaTabla.actualizarSimbolo(simbolo)
                if isinstance(valor , Error): return valor
                condicion = self.condicion.interpretar(arbol,nuevaTabla)
                if isinstance(condicion, Error): return condicion
                
                if self.condicion.tipo != Tipos.BOOLEAN:
                    return Error("Semantico","La condicon no puede ser de tipo: "+self.condicion.tipo,self.fila,self.columna)
            else: 
                condicion = False
                break
        return None
    def traducir(self, arbol, tabla):
        auxGen = Traductor()
        traductor = auxGen.obtenerInstancia()
        traductor.nuevoComentario('Traduccion For')
        bandera = True
        entorno = tabla
        if tabla.getSimbolo(self.inicio.identificador):
            bandera = False
        nuevaTabla = TablaSimbolos('For',tabla)
        inicio = self.inicio.traducir(arbol, nuevaTabla)
        if isinstance(inicio,Error): return inicio
        condicion= self.condicion.traducir(arbol, nuevaTabla)
        if isinstance(condicion,Error):return condicion
        
        if self.condicion.tipo != Tipos.BOOLEAN:
            return Error('Semantico', 'Condicion no booleana',self.fila,self.columna,datetime.now().date())
        while condicion:
            pass