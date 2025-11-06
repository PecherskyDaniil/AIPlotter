
from ..core.validator import validator
from .abstract_filter_model import AbstractFilterModel
class TemporalRangeFilterModel(AbstractFilterModel):
    __operator: str = "TEMPORAL RANGE"

    def __init__(self):
        super().__init__()
        self.operator="TEMPORAL RANGE"

    @property
    def operator(self) -> str:
        return self.__operator
    
    @operator.setter
    def operator(self, value: str):
        validator.validate_object_type(value, str)
        self.__operator = value

    def to_json(self):
        data={}
        data["expressionType"]="SIMPLE"
        data["subject"]=self.subject
        data["operator"]="TEMPORAL_RANGE"
        data["operatorId"]="TEMPORAL_RANGE"
        data["comparator"]=self.comparator
        data["clause"]="WHERE"
        data["sqlExpression"]=None
        data["isExtra"]=False
        data["isNew"]=False
        return data