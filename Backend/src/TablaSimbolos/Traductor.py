class Traductor:
    traductor = None
    def __init__(self):
        self.contTempo = 0
        self.contLbl = 0
        
        self.codigo = ''
        self.funciones = ''
        self.nativas = ''
        self.enFuncion = False
        self.enNativas = False
        self.temporales = []
        
        self.imprimirString = False
        self.compareString = False
        self.manejoError = False
        self.upper = False
        self.lower = False
        
        self.importaciones = []
        self.importaciones2 = ['fmt','math']
        
    #para hacerlo singleton
    def obtenerInstancia(self):
        if Traductor.traductor == None:
            Traductor.traductor = Traductor()
        return Traductor.traductor
    
    def limpiarTodo(self):
        self.contTempo = 0
        self.codigo = ''
        self.temporales = []
        self.imprimirString = False
        self.compareString = False
        self.manejoError = False
        self.upper = False
        self.lower = False
        
        self.importaciones = []
        self.importaciones2 = ['fmt','math']
        #Traductor.traductor = Traductor
        
    def setImportacion(self,libreria):
        if libreria in self.importaciones2:
            self.importaciones2.remove(libreria)
        else:
            return
        codigo = f'import(\n\t"{libreria}"\n\t)'
        
    def encabezado(self):
        codigo = '/*------ HEADER -------*/\npackage main;\n\n\n'
        if len(self.importaciones)>0:
            for impor in self.importaciones:
                codigo += impor
        if len(self.temporales)>0:
            codigo += 'var '
            for temporal in self.temporales:
                codigo += temporal+ ','
            codigo = codigo[:-1]
            codigo+= " float64; \n\n"
            
        codigo += 'var P, H float64; \nvar stack[30101999] float64;\nvar heap[30101999] float64;\n'
        return codigo
    
    def getCodigo(self):
        return f'{self.encabezado()}{self.nativas}{self.funciones}\nfunc main(){{\n{self.codigo}\n}}'
    
    def codeIn(self,codigo, tab = '\t'):
        if self.enNativas:
            if self.nativas == '':
                self.nativas = self.nativas + '/*----- Funciones Nativas ------*/\n'
            self.nativas = self.nativas +tab+codigo
        elif self.enFuncion:
            if self.funciones == '':
                self.funciones = self.funciones + '/*------ Funciones ------- */\n'
            self.funciones = self.funciones +tab+codigo
        else: 
            self.codigo = self.codigo +tab+codigo
    
    def nuevoComentario(self,comentario):
        self.codeIn(f'/*{comentario}*/\n')
        
    def agregarEspacio(self):
        self.codeIn('\n')
        
        
    def agregarTemporal(self):
        temp = f't{self.contTempo}'
        self.contTempo +=1
        self.temporales.append(temp)
        return temp
        
        
    def nuevaEtiqueta(self):
        lbl = f'L{self.contLbl}'
        self.contLbl += 1
        return lbl
    
    def colocarEtiqueta(self, lbl):
        self.codeIn(f'{lbl}:\n')
    def agregarIdentacion(self):
        self.codeIn('')
        
    #saltos
    def agregarGoto(self,lbl):
        self.codeIn(f'goto {lbl};\n')
    
    #para expresiones 
    def agregarExpresion(self, resultado, izquierda, derecha, operador):
        self.codeIn(f'{resultado} = {izquierda} {operador} {derecha};\n')
    
    #asignacion
    def agregarAsignacion(self, resultado , izquierda):
        self.codeIn(f'{resultado} = {izquierda};\n')
    
    #if 
    def agregarIf(self, izquierda, derecha, operador, lbl):
        self.codeIn(f'if {izquierda} {operador} {derecha} {{goto {lbl};}}\n')
        
    #funciones 
    def agregarInicioF(self, id):
        if not self.enNativas:
            self.enFuncion = True
        self.codeIn(f'func {id}(){{\n')
    def agregarFinF(self):
        self.codeIn(f'return;\n}}\n')
        if not self.enNativas:
            self.enFuncion = False
            
    #para stack
    
    def setStack(self, pos, valor):
        self.codeIn(f'stack[int({pos})] = {valor};\n')
        
    def getStack(self,lugar, pos):
        self.codeIn(f'{lugar} = stack[int({pos})];\n')
        
    #entornos
    def nuevoEntorno(self,tamano):
        self.codeIn(f'P = P + {tamano};\n')
        
    def llamarFun(self, id):
        self.codeIn(f'{id}();\n')
        
    def retornarEntorno(self, tamano):
        self.codeIn(f'P = P - {tamano};\n')
        
    #heap
    
    def setHeap(self, pos, valor):
        self.codeIn(f'heap[int({pos})] = {valor};\n')
        
    def getHeap(self, lugar, pos):
        self.codeIn(f'{lugar} = heap[int({pos})];\n')
        
    def siguienteHeap(self):
        self.codeIn(f'H = H +1;\n')
        
        
    def agregarImprimir(self, tipo, valor):
        self.setImportacion('fmt')
        self.codeIn(f'fmt.Printf("%{tipo}",{valor});\n')
        
    def imprimirCaracter(self, valor):
        self.setImportacion('fmt')
        self.codeIn(f'fmt.Printf("%c", int({valor}));\n')
        
    def imprimirTrue(self):
        self.setImportacion('fmt')
        self.agregarIdentacion()
        self.agregarImprimir("c", 116)
        self.agregarIdentacion()
        self.agregarImprimir("c", 114)
        self.agregarIdentacion()
        self.agregarImprimir("c", 117)
        self.agregarIdentacion()
        self.agregarImprimir("c", 101)
        
    def imprimirFalse(self):
        self.setImportacion('fmt')
        self.agregarIdentacion()
        self.agregarImprimir("c", 102)
        self.agregarIdentacion()
        self.agregarImprimir("c", 97)
        self.agregarIdentacion()
        self.agregarImprimir("c", 108)
        self.agregarIdentacion()
        self.agregarImprimir("c", 115)
        self.agregarIdentacion()
        self.agregarImprimir("c", 101)
        
    # para las nativas 
    
    def fPrintString(self):
        self.setImportacion('fmt')
        if(self.imprimirString):
            return
        self.imprimirString = True
        self.enNativas = True

        self.agregarInicioF('printString')
        # Label para salir de la funcion
        returnLbl = self.nuevaEtiqueta()
        # Label para la comparacion para buscar fin de cadena
        compareLbl = self.nuevaEtiqueta()
        # Temporal puntero a Stack
        tempP = self.agregarTemporal()
        # Temporal puntero a Heap
        tempH = self.agregarTemporal()
        self.agregarExpresion(tempP, 'P', '1', '+')
        self.getStack(tempH, tempP)
        # Temporal para comparar
        tempC = self.agregarTemporal()
        self.colocarEtiqueta(compareLbl)
        self.agregarIdentacion()
        self.getHeap(tempC, tempH)
        self.agregarIdentacion()
        self.agregarIf(tempC, '-1', '==', returnLbl)
        self.agregarIdentacion()
        self.imprimirCaracter(tempC)
        self.agregarIdentacion()
        self.agregarExpresion(tempH, tempH, '1', '+')
        self.agregarIdentacion()
        self.agregarGoto(compareLbl)
        self.colocarEtiqueta(returnLbl)
        self.agregarFinF()
        self.enNativas = False
        
    def fcompareString(self):
        if self.compareString:
            return
        self.compareString = True
        self.enNativas = True

        self.agregarInicioF("compareString")
        # Label para salir de la funcion
        returnLbl = self.nuevaEtiqueta()

        t2 = self.agregarTemporal()
        self.agregarExpresion(t2, 'P', '1', '+')
        t3 = self.agregarTemporal()
        self.getStack(t3, t2)
        self.agregarExpresion(t2,t2,'1', '+')
        t4 = self.agregarTemporal()
        self.getStack(t4, t2)

        l1 = self.nuevaEtiqueta()
        l2 = self.nuevaEtiqueta()
        l3 = self.nuevaEtiqueta()
        self.colocarEtiqueta(l1)

        t5 = self.agregarTemporal()
        self.agregarIdentacion()
        self.getHeap(t5,t3)

        t6 = self.agregarTemporal()
        self.agregarIdentacion()
        self.getHeap(t6,t4)

        self.agregarIdentacion()
        self.agregarIf(t5,t6,'!=', l3)
        self.agregarIdentacion()
        self.agregarIf(t5,'-1', '==', l2)

        self.agregarIdentacion()
        self.agregarExpresion(t3, t3,'1', '+')
        self.agregarIdentacion()
        self.agregarExpresion(t4, t4,'1','+')
        self.agregarIdentacion()
        self.agregarGoto(l1)

        self.colocarEtiqueta(l2)
        self.agregarIdentacion()
        self.setStack('P', '1')
        self.agregarIdentacion()
        self.agregarGoto(returnLbl)
        self.colocarEtiqueta(l3)
        self.agregarIdentacion()
        self.setStack('P', '0')
        self.colocarEtiqueta(returnLbl)
        self.agregarFinF()
        self.enNativas = False