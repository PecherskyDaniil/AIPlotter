
from enum import Enum
class validator():
    @staticmethod
    def __sql_injection_keys():
        return ["update ","set","drop","delete","truncate"]

    @staticmethod
    def validate_object_type(instance:any,dtype:any):
        if instance is None:
            return
        if not isinstance(instance,dtype):
            if dtype.__bases__[0]==Enum and instance in [member.value for member in dtype]:
                return
            raise Exception(f"Wrong object data type. Expected {dtype}, but received {type(instance)}.")
    
    @staticmethod
    def validate_sql_injections(value:str):
        validator.validate_object_type(value,str)
        sql_injection_keys=validator.__sql_injection_keys()
        for sik in sql_injection_keys:
            if sik in value.lower():
                raise Exception(f"Trying for sql injection in string {value}")
    
    @staticmethod
    def required_keys(keys:list,obj:dict):
        for key in keys:
            if not(key in obj.keys()):
                raise Exception(f"Object doesnt have key {key}")
    
    @staticmethod
    def validate_dashboard_json(obj:dict):
        validator.required_keys(["sql","table_names","data"],obj)
        validator.required_keys(["dashboard"],obj["data"])
        validator.required_keys(["name","charts"],obj["data"]["dashboard"])
    
    @staticmethod
    def validate_chart_json(obj:dict):
        validator.required_keys(["sql","table_names","data"],obj)
        validator.required_keys(["chart"],obj["data"])
        validator.required_keys(["chart_type"],obj["data"]["chart"])