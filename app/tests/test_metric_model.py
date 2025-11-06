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

# Тесты для MetricModel
class TestMetricModel:
    def test_metric_model_initialization(self):
        """Test MetricModel initialization"""
        metric = MetricModel()
        assert metric.aggregate is None
        assert metric.column is None
    
    def test_metric_model_setters_valid(self):
        """Test MetricModel setters with valid types"""
        metric = MetricModel()
        column = ColumnModel()
        
        metric.aggregate = "SUM"
        metric.column = column
        
        assert metric.aggregate == "SUM"
        assert metric.column == column
    
    def test_metric_model_setters_invalid(self):
        """Test MetricModel setters with invalid types"""
        metric = MetricModel()
        
        with pytest.raises(Exception):
            metric.aggregate = 123  # Should fail - not str
        
        with pytest.raises(Exception):
            metric.column = "not_a_column"  # Should fail - not ColumnModel
