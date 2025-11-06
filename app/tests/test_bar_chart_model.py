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

# Тесты для BarChartModel
class TestBarChartModel:
    def test_bar_chart_model_initialization(self):
        """Test BarChartModel initialization"""
        bar_chart = BarChartModel()
        assert bar_chart.x_axis is None
        assert bar_chart.metrics == []
        assert bar_chart.viz_type == VizType.BAR
        assert bar_chart.group_by == []
    
    def test_bar_chart_model_inheritance(self):
        """Test BarChartModel inherits from AbstractChartModel"""
        bar_chart = BarChartModel()
        assert isinstance(bar_chart, AbstractChartModel)
    
    def test_bar_chart_model_metrics_validation(self):
        """Test BarChartModel metrics list validation"""
        bar_chart = BarChartModel()
        
        # Valid metrics
        valid_metrics = [MetricModel(), MetricModel()]
        bar_chart.metrics = valid_metrics
        assert bar_chart.metrics == valid_metrics
        
        # Invalid metrics
        with pytest.raises(Exception):
            bar_chart.metrics = [MetricModel(), "not_a_metric"]
    
    def test_bar_chart_model_group_by_validation(self):
        """Test BarChartModel group_by list validation"""
        bar_chart = BarChartModel()
        
        # Valid group_by
        valid_group_by = ["category", "region"]
        bar_chart.group_by = valid_group_by
        assert bar_chart.group_by == valid_group_by
        
        # Invalid group_by
        with pytest.raises(Exception):
            bar_chart.group_by = ["valid", 123]  # Contains non-string


