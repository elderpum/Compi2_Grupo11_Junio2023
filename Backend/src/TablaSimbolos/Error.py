class Error():
    def __init__(self,tipo,descripcion, linea, columna, fecha):
        self.tipo = tipo
        self.descripcion = descripcion
        self.linea = linea
        self.columna = columna
        self.fecha = fecha
        
    def toString(self):
        return self.tipo + ' -- '+ self.descripcion + ' fila: '+str(self.linea)+', columna: ' +str(self.columna)