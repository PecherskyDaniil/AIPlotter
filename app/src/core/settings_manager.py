import configparser
from .logger import get_logger
from .validator import validator
from ..models.settings_model import SettingsModel
class SettingsManager():
    __filename=""
    __settings:SettingsModel
    def __init__(self):
        self.settings=SettingsModel()
        self.logger=get_logger("SettingsManager")

    def __new__(cls,*args,**kwargs):
        """
        Magic function for singeltone
        """
        if not hasattr(cls,'instance'):
            cls.instance=super(SettingsManager,cls).__new__(cls)
        return cls.instance
    
    @property
    def filename(self)->str:
        return self.__filename
    
    @filename.setter
    def filename(self,value:str):
        validator.validate_object_type(value,str)
        self.__filename=value
    
    @property
    def settings(self)->SettingsModel:
        return self.__settings
    
    @settings.setter
    def settings(self,value:SettingsModel):
        validator.validate_object_type(value,SettingsModel)
        self.__settings=value

    def load(self):
        try:
            config=configparser.ConfigParser()
            config.read(self.filename)
            self.settings.superset_host=config["Superset"]["host"]
            self.settings.superset_port=int(config["Superset"]["port"])
            self.settings.superset_username=config["Superset"]["username"]
            self.settings.superset_password=config["Superset"]["password"]
            self.settings.image_directory=config["DEFAULT"]["image_directory"]
            self.settings.upload_dir=config["DEFAULT"]["upload_dir"]
            self.logger.info("Data successfuly loaded from config file")
            return True
        except Exception as e:
            self.logger.error(f"Error while trying to fetc config file {e}")
            return False
        
        

   