class NodeAST(object):

    def __init__(self, valor_):
        self.valor = valor_
        self.hijos = []

    def setHijos(self, hijos):
        self.hijos = hijos

    def setValor(self, cadena_):
        self.valor = cadena_


    def addHijo(self, cadena_):
        self.hijos.append(NodeAST(cadena_))

    def addHijos(self, hijos_):
        for m in hijos_:
            self.hijos.append(m)

    def addHijoNodo(self, hijo_):
        self.hijos.append(hijo_)

    def getValor(self):
        return self.valor

    def getHijos(self):
        return self.hijos
