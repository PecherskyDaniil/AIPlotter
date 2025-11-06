

from .abstract_filter_model import AbstractFilterModel
class DefaultFilterModel(AbstractFilterModel):
    
    def __init__(self):
        super().__init__()
    
    def to_json(self):
        data={}
        data["expressionType"]="SIMPLE"
        data["subject"]=self.subject
        data["operator"]=self.operator
        data["operatorId"]=self.operator
        data["comparator"]=self.comparator
        data["clause"]="WHERE"
        data["sqlExpression"]=None
        data["isExtra"]=False
        data["isNew"]=False
        return data