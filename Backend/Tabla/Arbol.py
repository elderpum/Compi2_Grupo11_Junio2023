from .Errores import Error
from .Tabla_simbolos import TablaSimbolo
from .Lista_simbolos import List_Simbolo
from .NodeAST import NodeAST
import re
class Arbol(object):

    def __init__(self, instrucciones_):
        self.instrucciones = instrucciones_
        self.consola = ""
        self.tabla_global = TablaSimbolo(None,"GLOBAL")
        self.errores = []
        self.memoria = {}
        self.Lista_Simbolo = List_Simbolo()
        self.raiz = NodeAST("INIT")
        self.grafo = ""
        self.PilaCiclo = []
        self.PilaFunc = []
        self.c = 0
        
    def ejecutar(self):
        Instrucciones = NodeAST("INSTRUCCIONES")
        for inst in self.getInstrucciones():
            res = inst.Ejecutar(self, self.getGlobal())
            if isinstance(res, Error):
                self.errores.append(res)
            try:
                nodoInstruccion = NodeAST("INSTRUCCION")
                nodoInstruccion.addHijoNodo(inst.getNodo())
                Instrucciones.addHijoNodo(nodoInstruccion)
            except Exception as e:
                print(e)
        self.raiz.addHijoNodo(Instrucciones)
        x = 1
        for er in self.errores:
            er.numero = x
            x+=1

    def getInstrucciones(self):
        return self.instrucciones

    def getConsola(self):
        return self.consola

    def updateConsola(self, update_):
        self.consola = f"{self.consola}{update_}"

    def getGlobal(self):
        return self.tabla_global
    
    
    def graphAST(self):
        return self.getDot(self.raiz)
        
    def getDot(self, raiz_):
    
        self.grafo = ""
        self.grafo += "digraph G{\n"
        res = r'\"';
        self.grafo += "n0[label=\"" +  re.sub(res, '\\\"', raiz_.getValor()) + "\"];\n";
        self.c = 1;
        self.recorrerAST("n0",raiz_);
        self.grafo += "}";
        return self.grafo;
    
    
    def recorrerAST(self,padre_ , nPadre_):
        for hijo in nPadre_.getHijos():
            nombreHijo = "n" + str(self.c);
            res = r'\"'; 
            self.grafo += nombreHijo + "[label=\"" + re.sub(res, '\\\"', hijo.getValor())+ "\"];\n";
            self.grafo += padre_ + "->" + nombreHijo + ";\n";
            self.c+=1
            self.recorrerAST(nombreHijo,hijo);
        
    