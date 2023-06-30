class SimboloC():
    def __init__(self, identificador, tipo, posicion, globalVar, inHeap):
        self.identificador = identificador
        self.tipo = tipo
        self.posicion = posicion
        self.isGlobal = globalVar
        self.inHeap = inHeap
        self.value = None
        self.tipoAux = ''
        self.length = 0
        self.referencia = False
        self.params = None
    def getTipo(self):
        return self.tipo
    def getId(self):
        return self.identificador
    def getPos(self):
        return self.posicion
    def getInHeap(self):
        return self.inHeap
    
    def getParams(self):
        return self.params
    
    def setParams(self, params):
        self.params = params
    
    def setTipo(self, tipo):
        self.tipo = tipo
    def setId(self, id):
        self.identificador = id
    def setPos(self, pos):
        self.posicion = pos
    def setInHeap(self, value):
        self.inHeap = value
    
    def setTipoAux(self, tipo):
        self.tipoAux = tipo

    def getTipoAux(self):
        return self.tipoAux

    def setLength(self, length):
        self.length = length
    def getLength(self):
        return self.length

    def setReferencia(self, ref):
        self.referencia = ref   
        
    def getReferencia(self):
        return self.referencia
    
    def getValue(self):
        return self.value
    def setValue(self, value):
        self.value = value
class Simbolo():
    def __init__(self, identificador, tipo, valor,entorno, fila, columna):
        self.identificador = identificador
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.entorno = entorno
        self.columna = columna
        
    #getters
    def getEntorno(self):
        return self.entorno
    def getIdentificador(self):
        return self.identificador
    def getTipo(self):
        return self.tipo
    def getValor(self):
        return self.valor
    def getFila(self):
        return self.fila
    def getColumna(self):
        return self.columna
    
    #setters
    def setEntorno(self, entorno):
        self.entorno = entorno
    def setIdentificador(self, identificador):
        self.identificador = identificador
    def setValor(self, valor):
        self.valor = valor
    def setTipo(self, tipo):
        self.tipo = tipo
    def setFila(self, fila):
        self.fila = fila
    def setColumna(self, columna):
        self.columna = columna