
from ..core.validator import validator
import random
import string

from .abstract_chart_model import AbstractChartModel
from .chart_factory import ChartFactory
import json
import uuid
class DashboardModel:
    __name: str = uuid.uuid4().hex#''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
    __charts: list[AbstractChartModel] = []


    def __init__(self):
        self.name=uuid.uuid4().hex
        self.charts=[]
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        validator.validate_object_type(value, str)
        self.__name = value

    @property
    def charts(self) -> list[AbstractChartModel]:
        return self.__charts
    
    @charts.setter
    def charts(self, value: list[AbstractChartModel]):
        validator.validate_object_type(value, list)
        # Проверяем что все элементы списка соответствуют типу AbstractChartModel
        for item in value:
            validator.validate_object_type(item, AbstractChartModel)
        self.__charts = value

    def from_model_dict(self,dict_obj:dict,datasource_obj:dict):
        chart_factory_instance=ChartFactory()
        if "name" in dict_obj.keys() and dict_obj["name"] is not None:
            self.name=dict_obj["name"]
        for chart_obj in dict_obj["charts"]:
            self.charts.append(chart_factory_instance.create(chart_obj,datasource_obj))

    def to_json(self):
        data={}
        data["certified_by"]= ""
        data["certification_details"]=""
        data["css"]=""
        data["dashboard_title"]=self.name
        data["slug"]=None
        
        json_metadata={}
        json_metadata["chart_configuration"]={}
        json_metadata["global_chart_configuration"]={}
        json_metadata["global_chart_configuration"]["chartsInScope"]=[]
        json_metadata["global_chart_configuration"]["scope"]= {
                                                                "rootPath": [
                                                                    "ROOT_ID"
                                                                ],
                                                                "excluded": []
                                                            }
        json_metadata["positions"]={}
        json_metadata["positions"]["ROOT_ID"]={}
        json_metadata["positions"]["ROOT_ID"]["type"]="ROOT"
        json_metadata["positions"]["ROOT_ID"]["id"]="ROOT_ID"
        json_metadata["positions"]["ROOT_ID"]["children"]=["GRID_ID"]

        json_metadata["positions"]["GRID_ID"]={}
        json_metadata["positions"]["GRID_ID"]["type"]="GRID"
        json_metadata["positions"]["GRID_ID"]["id"]="GRID_ID"
        json_metadata["positions"]["GRID_ID"]["parents"]=["ROOT_ID"]
        json_metadata["positions"]["GRID_ID"]["children"]=[]
        
        json_metadata["positions"]["HEADER_ID"]= {
                            "id": "HEADER_ID",
                            "type": "HEADER",
                            "meta": {
                                "text": self.name
                            }
                        }
        json_metadata["positions"]["DASHBOARD_VERSION_KEY"]="v2"
        json_metadata["refresh_frequency"]=0
        json_metadata["color_scheme_domain"]=[]
        json_metadata["expanded_slices"]= {}
        json_metadata["label_colors"]={}
        #json_metadata["shared_label_colors"]=[],
        json_metadata["timed_refresh_immune_slices"]= []
        json_metadata["cross_filters_enabled"]= True
        json_metadata["default_filters"]="{}"
        json_metadata["filter_scopes"]= {}
        for ind,chart in enumerate(self.charts):
            json_metadata["global_chart_configuration"]["chartsInScope"].append(chart.chart_id)
            if ind%2==0:
                row_id=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
                row={
                    "type": "ROW",
                    "id": "ROW-"+row_id,
                    "children": [],
                    "parents": [
                        "ROOT_ID",
                        "GRID_ID"
                    ],
                    "meta": {
                        "background": "BACKGROUND_TRANSPARENT"
                    }
                }
                json_metadata["positions"]["ROW-"+row_id]=row
                json_metadata["positions"]["GRID_ID"]["children"].append("ROW-"+row_id)
            chart_id=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
            json_metadata["positions"]["ROW-"+row_id]["children"].append("CHART-"+chart_id)
            json_metadata["positions"]["CHART-"+chart_id]={
                            "type": "CHART",
                            "id": "CHART-"+chart_id,
                            "children": [],
                            "parents": [
                                "ROOT_ID",
                                "GRID_ID",
                                "ROW-"+row_id
                            ],
                            "meta": {
                                "width": 8,
                                "height": 50,
                                "chartId": chart.chart_id,
                                "sliceName": chart.name
                            }
                        }

            json_metadata["chart_configuration"][str(chart.chart_id)]={
                        "id":chart.chart_id,
                        "crossFilters": {
                        "scope": "global",
                        "chartsInScope": []
                    }
                }
            for key in json_metadata["chart_configuration"].keys():
                if key!=str(chart.chart_id) and "chartsInScope" in json_metadata["chart_configuration"][key].keys():
                    json_metadata["chart_configuration"][key]["chartsInScope"].append(chart.chart_id)
        data["json_metadata"]=json.dumps(json_metadata)
        return data
        



