from ..core.validator import validator

class SettingsModel:
    __superset_host: str = None
    __superset_port: int = None
    __superset_username: str = None
    __superset_password: str = None
    __image_directory: str = ""
    __upload_dir:str=None
    def __init__(self):
        self.superset_host=None
        self.superset_port=None
        self.superset_password=None
        self.superset_username=None
        self.image_directory=""

    @property
    def upload_dir(self)->str:
        return self.__upload_dir

    @upload_dir.setter
    def upload_dir(self,value:str):
        validator.validate_object_type(value,str)
        self.__upload_dir=value

    @property
    def superset_host(self) -> str:
        return self.__superset_host
    
    @superset_host.setter
    def superset_host(self, value: str):
        validator.validate_object_type(value, str)
        self.__superset_host = value

    @property
    def superset_port(self) -> int:
        return self.__superset_port
    
    @superset_port.setter
    def superset_port(self, value: int):
        validator.validate_object_type(value, int)
        self.__superset_port = value

    @property
    def superset_username(self) -> str:
        return self.__superset_username
    
    @superset_username.setter
    def superset_username(self, value: str):
        validator.validate_object_type(value, str)
        self.__superset_username = value

    @property
    def superset_password(self) -> str:
        return self.__superset_password
    
    @superset_password.setter
    def superset_password(self, value: str):
        validator.validate_object_type(value, str)
        self.__superset_password = value

    @property
    def image_directory(self) -> str:
        return self.__image_directory
    
    @image_directory.setter
    def image_directory(self, value: str):
        validator.validate_object_type(value, str)
        self.__image_directory = value
