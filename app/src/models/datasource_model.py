from ..core.validator import validator
class DatasourceModel:
    __name: str = None
    __datasource_id: int = None
    __datasource_type: str = None

    def __init__(self):
        self.name=None
        self.datasource_id=None
        self.datasource_type=None
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        validator.validate_object_type(value, str)
        self.__name = value

    @property
    def datasource_id(self) -> int:
        return self.__datasource_id
    
    @datasource_id.setter
    def datasource_id(self, value: int):
        validator.validate_object_type(value, int)
        self.__datasource_id = value

    @property
    def datasource_type(self) -> str:
        return self.__datasource_type
    
    @datasource_type.setter
    def datasource_type(self, value: str):
        validator.validate_object_type(value, str)
        self.__datasource_type = value