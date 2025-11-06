import requests
import re
import random
import string
import json
from ..core.logger import get_logger
from ..core.validator import validator
import uuid
class SupersetConnector:
    __host:str=None
    __port:int=None
    __username:str=None
    __password:str=None
    __auth_token:str=None
    __refresh_token:str=None
    __csrf_token:str=None
    __session:requests.session=None
    __cache_tables:dict=None
    def __init__(self,host:str=None,port:int=None,username:str=None,password:str=None,session:requests.session=requests.Session()):
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        self.session=session
        self.logger=get_logger("superset_connecter")

    @property
    def host(self)->str:
        return self.__host
    
    @host.setter
    def host(self,value:str):
        validator.validate_object_type(value,str)
        self.__host=value
    
    @property
    def port(self)->int:
        return self.__port
    
    @port.setter
    def port(self,value:int):
        validator.validate_object_type(value,int)
        self.__port=value
    
    @property
    def username(self)->str:
        return self.__username
    
    @username.setter
    def username(self,value:str):
        validator.validate_object_type(value,str)
        self.__username=value
    
    @property
    def password(self)->str:
        return self.__password
    
    @password.setter
    def password(self,value:str):
        validator.validate_object_type(value,str)
        self.__password=value
    
    @property
    def auth_token(self)->str:
        return self.__auth_token
    
    @auth_token.setter
    def auth_token(self,value:str):
        validator.validate_object_type(value,str)
        self.__auth_token=value

    @property
    def refresh_token(self)->str:
        return self.__refresh_token
    
    @refresh_token.setter
    def refresh_token(self,value:str):
        validator.validate_object_type(value,str)
        self.__refresh_token=value

    @property
    def csrf_token(self)->str:
        return self.__csrf_token
    
    @csrf_token.setter
    def csrf_token(self,value:str):
        validator.validate_object_type(value,str)
        self.__csrf_token=value

    @property
    def session(self)->requests.session:
        return self.__session
    
    @session.setter
    def session(self,value:requests.session):
        self.__session=value

    def authorize(self):
        
        payload={
            "password": self.password,
            "provider": "db",
            "refresh": True,
            "username": self.username
        }
        url_auth=f"http://{self.host}:{self.port}/api/v1/security/login"
        try:
            auth_response =self.session.post(url_auth, json=payload)
            if auth_response.status_code!=200:
                self.logger.error(f"Cant login in superset with current username and password {auth_response.json()}")
                return False
            self.refresh_token = auth_response.json()["refresh_token"]
            self.access_token = auth_response.json()["access_token"]
            self.logger.info("Successfully get access token and refresh token")
            url_csrf=f"http://{self.host}:{self.port}/api/v1/security/csrf_token"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            csrf_reponse=self.session.get(url_csrf, headers=headers)
            if csrf_reponse.status_code!=200:
                self.logger.error(f"Cant get csrf token by access token {csrf_reponse.json()}")
                return False
            self.csrf_token=csrf_reponse.json()["result"]
            self.logger.info("Successfully get csrf token")
            return True
        except Exception as e:
            self.logger.error(f"Can't authorize because of {e}")
            return False
    

    def get_tables_list(self,update=False):
        if self.__cache_tables is None or update:
            get_tables_url=f"http://{self.host}:{self.port}/api/v1/dataset/?q=%7B%0A%20%20%22page_size%22%3A%2010000000%0A%7D"
            headers = {'Authorization': f'Bearer {self.access_token}'}
            tables_response=self.session.get(get_tables_url,headers=headers)
            tables=tables_response.json()
            if tables_response.status_code//100!=2:
                self.logger.error(f"Cant get list of datasets in superset {tables_response.json()}")
                return None
            tables_dict={}
            for table in tables["result"]:
                tables_dict[table["table_name"]]=table
            self.__cache_tables=tables_dict
            self.logger.info("Successfuly get list of datasets")
            return self.__cache_tables
        else:
            return self.__cache_tables


    def create_dataset(self,sql_query,table_names:list[str]=None):#''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        validator.validate_sql_injections(sql_query)
        schema=None
        database=None
        if table_names is None:
            get_table_names_pattern=r'(?i)(?:FROM|JOIN)\s+([\w.]+|`[^`]+`|\[[^\]]+\])'
            table_names = re.findall(get_table_names_pattern, sql_query)
        superset_tables=self.get_tables_list()
        if superset_tables is None:
            self.logger.error("Cant create dataset because of Cant get list of available tables")
            return False
        for table_name in table_names:
            if table_name in superset_tables.keys():
                if schema is not None and superset_tables[table_name]["schema"]!=schema:
                    self.logger.error("Cant create dataset because of Tables are from different schemas")
                    return False
                    #raise Exception("Tables are from different schemas")
                elif schema is None:
                    schema=superset_tables[table_name]["schema"]
                
                if database is not None and superset_tables[table_name]["database"]["id"]!=database:
                    self.logger.error("Cant create dataset because of Tables are from different databases")
                    return False
                    # raise Exception("Tables are from different databases")
                elif database is None:
                    database=superset_tables[table_name]["database"]["id"]
            else:
                self.logger.error("Cant create dataset because of There is not such table in superset")
                return False
                #raise Exception("There is not such table in superset")
        
        create_dataset_url=f"http://{self.host}:{self.port}/api/v1/dataset/"
        headers = {"Authorization": f"Bearer {self.access_token}",'Accept': 'application/json','X-CSRFToken': self.csrf_token,"Referer":f"{self.host}:{self.port}/api/v1/security/csrf_token/"}
        payload={
                "catalog": None,
                "database": database,
                "external_url": None,
                "is_managed_externally": False,
                "schema": schema,
                "sql": sql_query,
                "table_name":uuid.uuid4().hex
                }
        response=self.session.post(create_dataset_url,headers=headers,json=payload)
        if response.status_code//100!=2:
            self.logger.error(f"Cant create dataset on superset because of {response.json()}")
            return False
        self.logger.info(f"Successfully created dataset {response.json()['id']}")
        return response

    def create_chart(self,chart_obj:dict):
        create_chart_url=f"http://{self.host}:{self.port}/api/v1/chart"
        headers = {"Authorization": f"Bearer {self.access_token}",'Accept': 'application/json','X-CSRFToken': self.csrf_token,"Referer":f"{self.host}:{self.port}/api/v1/security/csrf_token/"}
        payload=chart_obj
        response=self.session.post(create_chart_url,headers=headers,json=payload)
        if response.status_code//100!=2:
            self.logger.error(f"Cant create chart on superset because of {response.json()}")
            return False
        self.logger.info(f"Successfully created chart {response.json()['id']}")
        return response

    def create_dashboard(self,dashboard_obj:dict):
        create_dashboard_url=f"http://{self.host}:{self.port}/api/v1/dashboard"
        headers = {"Authorization": f"Bearer {self.access_token}",'Accept': 'application/json','X-CSRFToken': self.csrf_token,"Referer":f"{self.host}:{self.port}/api/v1/security/csrf_token/"}
        payload=dashboard_obj
        response=self.session.post(create_dashboard_url,headers=headers,json=payload)
        if response.status_code//100!=2:
            self.logger.error(f"Cant create dashboard on superset because of {response.json()}")
            return False
        dashboard_id=response.json()["id"]
        json_metadata=json.loads(dashboard_obj["json_metadata"])
        get_chart_url=f"http://{self.host}:{self.port}/api/v1/chart/"
        update_chart_url=f"http://{self.host}:{self.port}/api/v1/chart/"
        for chart_id in json_metadata["chart_configuration"].keys():
            chart_response=self.session.get(get_chart_url+chart_id,headers=headers)
            chart_data=chart_response.json()["result"]
            if chart_response.status_code//100!=2:
                self.logger.error(f"Cant create dashboard on superset because cant get chart {chart_id}")
                return False
            chart_data["dashboards"].append(dashboard_id)
            chart_data.pop('changed_on_delta_humanized',None)
            chart_data.pop('id',None)
            chart_data.pop('owners',None)
            chart_data.pop('thumbnail_url',None)
            chart_data.pop('url',None)
            chart_put_response=self.session.put(update_chart_url+chart_id,headers=headers,json=chart_data)
            if chart_put_response.status_code//100!=2:
                self.logger.error(f"Cant create dashboard on superset because cant update chart {chart_id}")
                return False
        self.logger.info(f"Successfully created dashboard {response.json()['id']}")
        return response

            





