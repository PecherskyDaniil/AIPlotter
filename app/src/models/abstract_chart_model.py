
from ..core.validator import validator
import random
import string
from .datasource_model import DatasourceModel
from .abstract_filter_model import AbstractFilterModel
from enum import Enum
import uuid
class VizType(Enum):
    TABLE= "table"
    LINE= "echarts_timeseries_line"
    BAR= "echarts_timeseries_bar"
    PIE="pie"
    SCATTER="echarts_timeseries_scatter"
    AREA="echarts_timeseries_area"
    NUMBER="big_number_total"
    NONE=None


class AbstractChartModel:
    __name: str = None#''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
    __viz_type: VizType = None
    __datasource: DatasourceModel = None
    __filters: list[AbstractFilterModel] = []
    __chart_id: int = None

    def __init__(self):
        self.name=uuid.uuid4().hex
        self.viz_type=None
        self.datasource=None
        self.filters=[]
        self.chart_id=None
    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str):
        validator.validate_object_type(value, str)
        self.__name = value

    @property
    def viz_type(self) -> VizType:
        return self.__viz_type
    
    @viz_type.setter
    def viz_type(self, value: VizType):
        validator.validate_object_type(value, VizType)
        self.__viz_type = value

    @property
    def datasource(self) -> DatasourceModel:
        return self.__datasource
    
    @datasource.setter
    def datasource(self, value: DatasourceModel):
        validator.validate_object_type(value, DatasourceModel)
        self.__datasource = value

    @property
    def filters(self) -> list[AbstractFilterModel]:
        return self.__filters
    
    @filters.setter
    def filters(self, value: list[AbstractFilterModel]):
        validator.validate_object_type(value, list)
        for item in value:
            validator.validate_object_type(item, AbstractFilterModel)
        self.__filters = value

    @property
    def chart_id(self) -> int:
        return self.__chart_id
    
    @chart_id.setter
    def chart_id(self, value: int):
        validator.validate_object_type(value, int)
        self.__chart_id = value

    def from_model_dict(self,dict_obj:dict):
        pass

    def to_json(self):
        pass