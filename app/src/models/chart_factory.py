
from .abstract_chart_model import AbstractChartModel
from .bar_chart_model import BarChartModel
from .scatter_chart_model import ScatterChartModel
from .pie_chart_model import PieChartModel

class ChartFactory:

    viz_type_to_model={
    "bar":BarChartModel,
    "scatter":ScatterChartModel,
    "pie":PieChartModel
    }

    def create(self,dict_obj:dict,datasource_obj:dict)->AbstractChartModel:
        chart_obj=self.viz_type_to_model[dict_obj["chart_type"]]()
        chart_obj.from_model_dict(dict_obj,datasource_obj)
        return chart_obj