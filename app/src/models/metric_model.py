
from ..core.validator import validator
from .column_model import ColumnModel

class MetricModel:
    __aggregate: str = None
    __column: ColumnModel = None

    def __init__(self):
        self.aggregate=None
        self.column=None
    @property
    def aggregate(self) -> str:
        return self.__aggregate
    
    @aggregate.setter
    def aggregate(self, value: str):
        validator.validate_object_type(value, str)
        self.__aggregate = value

    @property
    def column(self) -> ColumnModel:
        return self.__column
    
    @column.setter
    def column(self, value: ColumnModel):
        validator.validate_object_type(value, ColumnModel)
        self.__column = value

    def to_json(self):
        data={}
        data["expressionType"]= "SIMPLE"
        data["aggregate"]= self.aggregate.upper()
        data["sqlExpression"]=None
        data["datasourceWarning"]= False,
        data["hasCustomLabel"]=False,
        data["label"]= f"{self.aggregate.upper()}({self.column.name})"
        data["column"]=self.column.to_json()
        return data