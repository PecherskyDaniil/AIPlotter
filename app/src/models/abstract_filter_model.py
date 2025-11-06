
from ..core.validator import validator
from enum import Enum

class Operator(Enum):
    IN="IN"
    NOT_IN="NOT IN"
    EQ="="
    TIME_RANGE="TEMPORAL_RANGE"

class AbstractFilterModel:
    __operator: Operator = None
    __subject: str = None
    __comparator: str = None


    def __init__(self):
        self.operator=None
        self.subject=None
        self.comparator=None
    @property
    def operator(self) -> Operator:
        return self.__operator
    
    @operator.setter
    def operator(self, value: Operator):
        validator.validate_object_type(value, Operator)
        self.__operator = value

    @property
    def subject(self) -> str:
        return self.__subject
    
    @subject.setter
    def subject(self, value: str):
        validator.validate_object_type(value, str)
        self.__subject = value

    @property
    def comparator(self) -> str:
        return self.__comparator
    
    @comparator.setter
    def comparator(self, value):
        self.__comparator = value

    def to_json(self):
        pass