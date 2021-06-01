classHighlither = '###'
endOfClass = '____'

class ToString():
    def __str__(self):
        return ModelToStringConverter().convert(self) # pragma: no cover

class ModelToStringConverter:
    def convert(self, model):
        strings =[]
        strings.append( self.getClassText(model))
        strings.append('')
        attributes = self.getAllAttributes(model)
        [strings.append(self.getMethodText(model, attr)) for attr in attributes]
        strings.append(endOfClass)
        string = '\n'.join(strings)
        return string

    def getClassText(self,model):
        string = classHighlither + ' ' + model.__class__.__name__ + ' ' + classHighlither
        return string

    def getAllAttributes(self, model):
        attr:str
        allAttributes = dir(model)
        allAttributes = [attr for attr in allAttributes if not attr.startswith('__')]
        return allAttributes

    def getMethodText(self,model, methodName: str):
        value = getattr(model, methodName)
        valueString = self.getValueText(value)
        string = methodName + ' ' +  str(type(value)) +': ' + valueString
        return string
    
    def getValueText(self, value):
        if isinstance(value, float):
            return str(round(value,2))

        string = str(value)
        if len(string)>20:
            return string[:20] + ' ...'
        return str(value)