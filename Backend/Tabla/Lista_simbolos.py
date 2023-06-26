from .Nodo_list import Node_list


class List_Simbolo(object):

    def __init__(self):
        self.Lista = {}

    def Agregar(self, simbolo_: Node_list):
        try:
            self.Lista[simbolo_.nombre +"-"+ simbolo_.ambito]
            self.Lista[simbolo_.nombre +"-"+ simbolo_.ambito] = simbolo_
        except:
            simbolo_.numero = len(self.Lista)+1
            self.Lista[simbolo_.nombre +"-"+ simbolo_.ambito] = simbolo_
        return
    
    def getLista(self):
        return list(self.Lista.values())