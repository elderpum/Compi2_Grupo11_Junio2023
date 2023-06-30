from ..TablaSimbolos.Error import Error
from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Simbolo import Simbolo
from ..Helpers.TiposDatos import Tipos
from ..TablaSimbolos.Traductor import Traductor
from ..Helpers.ReturnCo import ReturnCo
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
        genAux = Traductor()
        traductor = genAux.obtenerInstancia()
        
        if self.valores:
            if isinstance(self.tipo, list):
                if self.array == self.tipo[0]:
                    traductor.nuevoComentario('Compilacion del Array')
                    t0 = traductor.agregarTemporal()
                    t1 = traductor.agregarTemporal()
                    traductor.agregarAsignacion(t0,'H')
                    traductor.agregarExpresion(t1,t0,'1','+')
                    traductor.setHeap('H', len(self.valores))
                    apuntador = str(len(self.valores)+1)
                    traductor.agregarExpresion('H','H',apuntador,'+')
                    traductor.agregarEspacio()
                    length = 0
                    for valor in self.valores:
                        if not isinstance(DeclaracionArreglo):
                            valo = valor.traducir(arbol, tabla)
                            if isinstance(valo,Error): return valo
                            try:
                                if valo.getTipo() == self.tipo[1]:
                                    traductor.setHeap(t1,valo.getValue())
                                    traductor.agregarExpresion(t1,t1,'1','+')
                                    traductor.agregarEspacio()
                                    length += 1.
                                else:
                                    return Error("Semantico", "Tipos no coinciden en declaracion o asignacion del array", self.fila, self.columna)
                            except:
                                pass
                    simbolo = tabla.setTabla(self.id,self.tipo,True)
                    simbolo.setTipoAux(self.tipo[1])
                    simbolo.setLength(length)
                    tempPos = simbolo.posicion
                    if not simbolo.isGlobal:
                        tempPos = traductor.agregarTemporal()
                        traductor.agregarExpresion(tempPos, 'P', simbolo.posicion, "+")
                    traductor.setStack(tempPos, t0)
                    traductor.nuevoComentario('Fin de la compilacion del Array')
            else:
                traductor.nuevoComentario('Compilacion del Array')
                t0 = traductor.agregarTemporal()
                t1 = traductor.agregarTemporal()
                traductor.agregarAsignacion(t0,'H')
                traductor.agregarExpresion(t1,t0,'1','+')
                traductor.setHeap('H', len(self.valores))
                apuntador = str(len(self.valores)+1)
                traductor.agregarExpresion('H','H',apuntador,'+')
                traductor.agregarEspacio()
                length = 0
                tipoAux = []
                tipoAux.append('array')
                aux = ''
                for value in self.valores:
                    if not isinstance(value, DeclaracionArreglo):
                        if isinstance(value, list):
                            for v in value:
                                
                                val = v.traducir(arbol,tabla)
                                if isinstance(val, Error): return val
                                aux = val.getType()
                                traductor.setHeap(t1,val.getValue())
                                traductor.agregarExpresion(t1,t1,'1','+')
                                traductor.agregarEspacio()
                                length += 1
                        else:
                            val = value.traducir(arbol,tabla)
                            if isinstance(val, Error): return val
                            aux = val.getType()
                            traductor.setHeap(t1,val.getValue())
                            traductor.agregarExpresion(t1,t1,'1','+')
                            traductor.agregarEspacio()
                            length += 1
                    else:
                        value.multiDim = True
                        value.tipo = value.getTipo()
                        val = value.traducir(arbol,tabla)
                        if isinstance(val, Error): return val
                        tipoAux.append(val.getTipoAux())
                        traductor.setHeap(t1,val.getValue())
                        traductor.agregarExpresion(t1,t1,'1','+')
                        traductor.agregarEspacio()
                        length += 1
                tipoAux.append(aux)
                # if self.multiDim:
                #     return ReturnCo(t0, 'array', True, tipoAux)
                # if self.isinStruct == False:
                #     simbolo = tabla.setTabla(self.id,self.tipo,True)
                #     simbolo.setTipoAux(tipoAux)
                #     simbolo.setLength(length)
                #     tempPos = simbolo.pos
                #     if not simbolo.isGlobal:
                #         tempPos = traductor.addTemp()
                #         traductor.addExp(tempPos, 'P', simbolo.pos, "+")
                #     traductor.setStack(tempPos, t0)
                #     traductor.addComment('Fin de la compilacion del Array')
                #else:
                return ReturnCo(t0, 'array', True, tipoAux)

