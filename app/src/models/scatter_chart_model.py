import json
from ..core.validator import validator
from .abstract_chart_model import AbstractChartModel,VizType
from .metric_model import MetricModel
from .column_model import ColumnModel
from .default_filter_model import DefaultFilterModel
from .datasource_model import DatasourceModel
class ScatterChartModel(AbstractChartModel):
    __x_axis: str = None
    __metrics: list[MetricModel] = []
    __viz_type: VizType = VizType.SCATTER
    __group_by: list[str] = []

    def __init__(self):
        super().__init__()
        self.x_axis=None
        self.metrics=[]
        self.viz_type=VizType.SCATTER
        self.group_by=[]

    @property
    def x_axis(self) -> str:
        return self.__x_axis
    
    @x_axis.setter
    def x_axis(self, value: str):
        validator.validate_object_type(value, str)
        self.__x_axis = value

    @property
    def metrics(self) -> list[MetricModel]:
        return self.__metrics
    
    @metrics.setter
    def metrics(self, value: list[MetricModel]):
        validator.validate_object_type(value, list)
        # Проверяем что все элементы списка соответствуют типу MetricModel
        for item in value:
            validator.validate_object_type(item, MetricModel)
        self.__metrics = value

    @property
    def viz_type(self) -> VizType:
        return self.__viz_type
    
    @viz_type.setter
    def viz_type(self, value: VizType):
        validator.validate_object_type(value, VizType)
        self.__viz_type = value

    @property
    def group_by(self) -> list[str]:
        return self.__group_by
    
    @group_by.setter
    def group_by(self, value: list[str]):
        validator.validate_object_type(value, list)
        # Проверяем что все элементы списка соответствуют типу str
        for item in value:
            validator.validate_object_type(item, str)
        self.__group_by = value
    

    def from_model_dict(self,dict_obj:dict,datasource_obj:dict):
        self.x_axis=dict_obj["x_axis"]
        self.datasource=DatasourceModel()
        self.datasource.datasource_id=datasource_obj["id"]
        self.datasource.datasource_type="table"
        for metric in dict_obj["metrics"]:
            column_model_instance=ColumnModel()
            for column in datasource_obj["columns"]:
                if column["column_name"]==metric["column_name"]:
                    column_model_instance.name=metric["column_name"]
                    column_model_instance.column_id=column["id"]
                    column_model_instance.json=column
                    break
            metric_model_instance=MetricModel()
            metric_model_instance.column=column_model_instance
            metric_model_instance.aggregate=metric["aggregate"]
            self.metrics.append(metric_model_instance)
        for filter_obj in dict_obj["filters"]:
            filter_model_instance=DefaultFilterModel()
            filter_model_instance.subject=filter_obj["column"]
            filter_model_instance.operator=filter_obj["operator"]
            filter_model_instance.comparator=filter_obj["comparator"]
            self.filters.append(filter_model_instance)
        for group in dict_obj["group_by"]:
            self.group_by.append(group)

    def to_json(self):
        data={}
        data["slice_name"]=self.name
        data["viz_type"]=self.viz_type.value
        data["slice_name"]=self.name
        data["datasource_id"]=self.datasource.datasource_id
        data["datasource_type"]="table"
        params={}
        params["viz_type"]=self.viz_type.value
        params["datasource"]=f"{self.datasource.datasource_id}__{data['datasource_type']}"
        params["x_axis"]=self.x_axis
        params["groupby"]=self.group_by
        params["x_axis_sort_asc"]=True
        metrics=[]
        for metric_obj in self.metrics:
            metrics.append(metric_obj.to_json())
        params["metrics"]=metrics.copy()
        adhoc_filters=[]
        for filter_obj in self.filters:
            adhoc_filters.append(filter_obj.to_json())
        group_by=[]
        for group_obj in self.group_by:
            group_by.append(group_obj)
        params["group_by"]=group_by.copy()



        #params["x_axis_sort_series"]="name"
        params["x_axis_sort_series_ascending"]=True
        params["time_grain_sqla"]="P1D"
        params["x_axis_time_format"]="smart_date"
        params["y_axis_format"]= "SMART_NUMBER"
        params["rich_tooltip"]= True
        params["tooltipTimeFormat"]="smart_date"

        data["params"]=json.dumps(params)
        return data

    
