class Error(object):

    def __init__(self,tipo_, descripcion_, fila_, columna_):
        self.tipo = tipo_
        self.descripcion = descripcion_
        self.fila = fila_
        self.columna = columna_
        self.numero = 0
        
    def toString(self):
        return self.tipo + " - " + self.descripcion + " [" + self.fila + ", " + self.columna + "]\n"
