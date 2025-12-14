import requests
import re
import random
import string
import json
from ..core.logger import get_logger
from ..core.validator import validator
import uuid
from ..core.create_name import create_name
import datetime
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


    def check_token(self):
        get_url=f"http://{self.host}:{self.port}/api/v1/chart"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        response=self.session.get(get_url,headers=headers)
        if response.status_code//100!=2 and response.json()["msg"]=="Token has expired":
            return self.authorize()
        return True
        

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
    

    def get_table(self,table_name:str):
        self.check_token()
        get_table_url=f"http://{self.host}:{self.port}/api/v1/dataset/?q=(filters:!((col:table_name,opr:ct,value:{table_name})),order_column:changed_on_delta_humanized,order_direction:asc,page:0,page_size:10000)"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        tables_response=self.session.get(get_table_url,headers=headers).json()
        if len(tables_response["result"])!=0:
            return tables_response["result"][0]
        else:
            return None

    def get_tables_list(self,update=False):
        self.check_token()
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
        self.check_token()
        schema=None
        database=None
        if table_names is None:
            get_table_names_pattern=r'(?i)(?:FROM|JOIN)\s+([\w.]+|`[^`]+`|\[[^\]]+\])'
            table_names = re.findall(get_table_names_pattern, sql_query)
        for table_name in table_names:
            superset_table=self.get_table(table_name)
            if superset_table is not None:
                if schema is not None and superset_table["schema"]!=schema:
                    self.logger.error("Cant create dataset because of Tables are from different schemas")
                    return False
                    #raise Exception("Tables are from different schemas")
                elif schema is None:
                    schema=superset_table["schema"]
                
                if database is not None and superset_table["database"]["id"]!=database:
                    self.logger.error("Cant create dataset because of Tables are from different databases")
                    return False
                    # raise Exception("Tables are from different databases")
                elif database is None:
                    database=superset_table["database"]["id"]
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
                "table_name":create_name()
                }
        response=self.session.post(create_dataset_url,headers=headers,json=payload)
        if response.status_code//100!=2:
            self.logger.error(f"Cant create dataset on superset because of {response.json()}")
            return False
        self.logger.info(f"Successfully created dataset {response.json()['id']}")
        return response

    def create_chart(self,chart_obj:dict):
        self.check_token()
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
        self.check_token()
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

    def clean_from_objects(self,expire_time:datetime.timedelta):
        self.check_token()
        self.logger.info(f"Cleaning started")
        error_count=0
        get_dashboards_url=f"http://{self.host}:{self.port}/api/v1/dashboard/?q=(filters:!((col:dashboard_title,opr:ct,value:ai_plotter)),order_column:changed_on_delta_humanized,order_direction:asc,page:0,page_size:10000)"
        delete_dashboard_url=f"http://{self.host}:{self.port}/api/v1/dashboard/"
        error_count+=self.delete_objects(get_dashboards_url,delete_dashboard_url,expire_time)
        
        get_charts_url=f"http://{self.host}:{self.port}/api/v1/chart/?q=(filters:!((col:slice_name,opr:ct,value:ai_plotter)),order_column:changed_on_delta_humanized,order_direction:asc,page:0,page_size:10000)"
        delete_chart_url=f"http://{self.host}:{self.port}/api/v1/chart/"
        error_count+=self.delete_objects(get_charts_url,delete_chart_url,expire_time)
        
        get_dataset_url=f"http://{self.host}:{self.port}/api/v1/dataset/?q=(filters:!((col:table_name,opr:ct,value:ai_plotter)),order_column:changed_on_delta_humanized,order_direction:asc,page:0,page_size:10000)"
        delete_datset_url=f"http://{self.host}:{self.port}/api/v1/dataset/"
        error_count+=self.delete_objects(get_dataset_url,delete_datset_url,expire_time)

        self.logger.info(f"Cleaning ended with {error_count} errors")
    
    def delete_objects(self,get_url:str,delete_base_url:str,expire_time):
        error_count=0
        headers = {"Authorization": f"Bearer {self.access_token}",'Accept': 'application/json','X-CSRFToken': self.csrf_token,"Referer":f"{self.host}:{self.port}/api/v1/security/csrf_token/"}
        response=self.session.get(get_url,headers=headers).json()
        for obj in response["result"]:
            #print(datetime.datetime.now()-datetime.datetime.strptime(chart_obj["changed_on_utc"],"%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None))
            if (datetime.datetime.now()-datetime.datetime.strptime(obj["changed_on_utc"],"%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)).total_seconds()>expire_time.total_seconds():
                result=self.session.delete(delete_base_url+str(obj["id"]),headers=headers)
                if result.status_code//100!=2:
                    self.logger.error(f"Cant delete object by url {delete_base_url+str(obj['id'])}")
                    error_count+=1
                else:
                    self.logger.info(f"Successfully deleted object by url {delete_base_url+str(obj['id'])}")
        return error_count
            
    def execute_sql_query(self,query:str,database_id:int)->dict:
        self.check_token()
        url=f"http://{self.host}:{self.port}/api/v1/sqllab/execute"
        headers = {"Authorization": f"Bearer {self.access_token}",'Accept': 'application/json','X-CSRFToken': self.csrf_token,"Referer":f"{self.host}:{self.port}/api/v1/security/csrf_token/"}
        payload={"sql":query,"database_id":database_id,"queryLimit": 10}
        response=self.session.post(url,headers=headers,json=payload)
        if response.status_code//100!=2:
            self.logger.error(f"Cant execute this sql query {query} because of {response.content}")
            return False
        
        self.logger.info(f"Sql query executed succesfully")
        return response.json()





