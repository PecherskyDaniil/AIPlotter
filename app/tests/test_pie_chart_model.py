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

# Тесты для PieChartModel
class TestPieChartModel:
    def test_pie_chart_model_initialization(self):
        """Test PieChartModel initialization"""
        pie_chart = PieChartModel()
        assert pie_chart.metrics == []
        assert pie_chart.viz_type == VizType.PIE
        assert pie_chart.group_by == []
    
    def test_pie_chart_model_inheritance(self):
        """Test PieChartModel inherits from AbstractChartModel"""
        pie_chart = PieChartModel()
        assert isinstance(pie_chart, AbstractChartModel)
