from ..Abstracta.Abstracta import Abstracta
from ..TablaSimbolos.Traductor import Traductor
from ..TablaSimbolos.Error import Error
from ..Helpers.TiposDatos import Tipos

class Console(Abstracta):
    def __init__(self,expresiones, fila, columna):
        self.expresiones = expresiones
        super().__init__(fila, columna)
        
    def interpretar(self, arbol, tabla):
       # print(str(self.expresion)+"desde la claseeeeeee")
        if len(self.expresiones)>1:
            contenido = ""
            for expresion in self.expresiones:
                valor = expresion.interpretar(arbol,tabla)
                contenido= contenido +""+str(valor)
            arbol.updateConsola(str(contenido))
        else:
            valor = self.expresiones[0].interpretar(arbol, tabla)
            arbol.updateConsola(str(valor))

        return valor
    def traducir(self, arbol, tabla):
        genAux = Traductor()
        generador = genAux.obtenerInstancia()
        
        for valor in self.expresiones:
            value = valor.interpretar(arbol,tabla)
            if isinstance(value, Error): return value
            if valor.getTipo()  == Tipos.NUMBER:
                if isinstance(value,int) and not isinstance(value, bool):
                    generador.agregarImprimir('d',value)
                elif isinstance(value, float):
                    generador.agregarImprimir('f',value)
            elif valor.getTipo() == Tipos.STRING:
                generador.fPrintString()
                parametroTemporal = generador.agregarTemporal()
                generador.agregarExpresion(parametroTemporal, 'P', tabla.size, '+')
                generador.agregarExpresion(parametroTemporal, parametroTemporal, '1', '+')
                generador.setStack(parametroTemporal, str(value))
                
                generador.nuevoEntorno(tabla.size)
                generador.llamarFun('printString')

                temp = generador.agregarTemporal()
                generador.getStack(temp, 'P')
                generador.retornarEntorno(tabla.size)
            elif valor.getTipo() == Tipos.BOOLEAN:
                tempLbl = generador.nuevaEtiqueta()

                #generador.putLabel(value.getTrueLbl())
                generador.imprimirTrue()

                generador.agregarGoto(tempLbl)

                #generador.putLabel(value.getFalseLbl())
                generador.imprimirFalse()

                generador.colocarEtiqueta(tempLbl)
        generador.agregarImprimir('c', 10)