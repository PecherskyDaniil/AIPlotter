from ..core.validator import validator

class ColumnModel:

    __name:str=None
    __column_id:int=None
    __json:dict=None

    def __init__(self):
        self.name=None
        self.column_id=None
        self.json=None
    @property
    def name(self)->str:
        return self.__name
    
    @name.setter
    def name(self,value:str):
        validator.validate_object_type(value,str)
        self.__name=value

    @property
    def column_id(self)->int:
        return self.__column_id
    
    @column_id.setter
    def column_id(self,value:int):
        validator.validate_object_type(value,int)
        self.__column_id=value

    @property
    def json(self)->dict:
        return self.__json
    
    @json.setter
    def json(self,value:dict):
        validator.validate_object_type(value,dict)
        self.__json=value

    def to_json(self):
        return self.json