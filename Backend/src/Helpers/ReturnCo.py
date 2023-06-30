class ReturnCo:
    def __init__(self,val,retType,isTemp, auxType = "", length =0,referencia = ''):
        self.value = val
        self.type = retType
        self.auxType = auxType
        self.length = length
        self.referencia = referencia
        self.isTemp = isTemp
        self.trueLbl = ''
        self.falseLbl = ''
        
    def getValue(self):
        return self.value
    def getType(self):
        return self.type
    def getAuxType(self):
        return self.auxType
    def getIsTemp(self):
        return self.isTemp
    def getLength(self):
        return self.length
    def getReferencia(self):
        return self.referencia
    def getTrueLbl(self):
        return self.trueLbl
    def getFalseLbl(self):
        return self.falseLbl
    
    
    ###############################
    def setValue(self,value):
        self.value = value
    def setType(self,type):
        self.type = type
    def setAuxType(self,auxType):
        self.auxType = auxType
    def setIsTemp(self,isTemp):
        self.isTemp = isTemp
    def setLength(self,length):
        self.length = length
    def setReferencia(self,referencia):
        self.referencia = referencia
    def setTrueLbl(self,trueLbl):
        self.trueLbl = trueLbl
    def setFalseLbl(self,falseLbl):
        self.falseLbl = falseLbl