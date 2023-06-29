class Arbol: 
    
    def __init__(self, instrucciones):
        self.instrucciones = instrucciones
        self.funciones = []
        self.errores = []
        self.consola = ""
        self.tablaGlobal = None
        self.tablaInterpretada = {}
        
    def setTablaSimbolosGlobalInterpretada(self, entorno, valor):
        self.tablaInterpretada[entorno] = valor
    
    def getTablaSimbolosGlobalInterpretada(self):
        return self.tablaInterpretada
    
    def setInstrucciones(self, instrucciones):
        self.instrucciones = instrucciones
        
    def getInstrucciones(self):
        return self.instrucciones
    
    def getFunciones(self):
        return self.funciones
    
    def setFunciones(self, funciones):
        self.funciones.append(funciones)
        
    def getFuncion(self, identificador):
        for funcion in self.funciones:
            if funcion.identificador == identificador:
                return funcion
        return None
    
    def getErrores(self):
        return self.errores
    
    def setErrores(self, errores):
        self.errores.append(errores)
        
    def getConsola(self):
        return self.consola
    
    def setConsola(self, consola):
        self.consola = consola
    
    def updateConsola(self, consola):
        self.consola += consola + '\n'
    
    def getTablaGlobal(self):
        return self.tablaGlobal
    
    def setTablaGlobla(self, tabla):
        self.tablaGlobal = tabla