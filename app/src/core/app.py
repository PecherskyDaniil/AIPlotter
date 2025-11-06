
from ..core.validator import validator
from ..models.settings_model import SettingsModel
from ..superset.superset_connector import SupersetConnector
from .logger import get_logger
import os
class App:
    __connector:SupersetConnector
    __upload_dir:str=None
    def __init__(self):
        self.connector=SupersetConnector()
        self.logger=get_logger("AIPlotApp")

    def __new__(cls,*args,**kwargs):
        """
        Magic function for singeltone
        """
        if not hasattr(cls,'instance'):
            cls.instance=super(App,cls).__new__(cls)
        return cls.instance


    @property
    def upload_dir(self)->str:
        return self.__upload_dir

    @upload_dir.setter
    def upload_dir(self,value:str):
        validator.validate_object_type(value,str)
        self.__upload_dir=value

    @property
    def connector(self)->SupersetConnector:
        return self.__connector
    
    @connector.setter
    def connector(self,value:SupersetConnector):
        validator.validate_object_type(value,SupersetConnector)
        self.__connector=value


    def load_from_settings(self,settings:SettingsModel):
        try:
            self.connector.host=settings.superset_host
            self.connector.port=settings.superset_port
            self.connector.username=settings.superset_username
            self.connector.password=settings.superset_password
            self.upload_dir=settings.upload_dir
            self.logger.info("Settings succsessfully loaded to app")
            return True
        except Exception as e:
            self.logger.error(str(e))
            return False
    

    def start(self):
        if self.connector.authorize():
            os.makedirs(self.upload_dir+"/audio", exist_ok=True)
            self.logger.info("App is started")
        else:
            self.logger.error("Can't start app without auth")
            
    

