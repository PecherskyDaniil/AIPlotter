
from ..core.validator import validator
from ..models.settings_model import SettingsModel
from ..superset.superset_connector import SupersetConnector
from .logger import get_logger
import os
import uuid
import datetime

class App:
    __connector:SupersetConnector
    __upload_dir:str=None
    __object_expire_time:datetime.timedelta=None
    __clean_time_minutes:float=None
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


    @property
    def object_expire_time(self)->datetime.timedelta:
        return self.__object_expire_time
    
    @object_expire_time.setter
    def object_expire_time(self,value:datetime.timedelta):
        validator.validate_object_type(value,datetime.timedelta)
        self.__object_expire_time=value

    @property
    def clean_time_minutes(self):
        return self.__clean_time_minutes

    @clean_time_minutes.setter
    def clean_time_minutes(self,value):
        validator.validate_object_type(value,float)
        self.__clean_time_minutes=value

    def load_from_settings(self,settings:SettingsModel):
        try:
            self.connector.host=settings.superset_host
            self.connector.port=settings.superset_port
            self.connector.username=settings.superset_username
            self.connector.password=settings.superset_password
            self.upload_dir=settings.upload_dir
            self.object_expire_time=datetime.timedelta(minutes=settings.object_expire_time)
            self.clean_time_minutes=settings.clean_time_minutes
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
            
    

