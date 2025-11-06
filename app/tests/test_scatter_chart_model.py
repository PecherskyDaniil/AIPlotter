from ..src.models.abstract_chart_model import *
from ..src.models.abstract_filter_model import *
from ..src.models.bar_chart_model import *
from ..src.models.column_model import *
from ..src.models.dashboard_model import *
from ..src.models.datasource_model import *
from ..src.models.datetime_filter_model import *
from ..src.models.default_filter_model import *
from ..src.models.metric_model import *
from ..src.models.pie_chart_model import *
from ..src.models.scatter_chart_model import *
from ..src.models.settings_model import *
import pytest



# Тесты для ScatterChartModel
class TestScatterChartModel:
    def test_scatter_chart_model_initialization(self):
        """Test ScatterChartModel initialization"""
        scatter_chart = ScatterChartModel()
        assert scatter_chart.x_axis is None
        assert scatter_chart.metrics == []
        assert scatter_chart.viz_type == VizType.SCATTER
        assert scatter_chart.group_by == []
    
    def test_scatter_chart_model_inheritance(self):
        """Test ScatterChartModel inherits from AbstractChartModel"""
        scatter_chart = ScatterChartModel()
        assert isinstance(scatter_chart, AbstractChartModel)
