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


# Тесты для TemporalRangeFilterModel
class TestTemporalRangeFilterModel:
    def test_temporal_range_filter_default_operator(self):
        """Test TemporalRangeFilterModel has correct default operator"""
        temporal_filter = TemporalRangeFilterModel()
        assert temporal_filter.operator == "TEMPORAL RANGE"
    
    def test_temporal_range_filter_operator_validation(self):
        """Test TemporalRangeFilterModel operator validation"""
        temporal_filter = TemporalRangeFilterModel()
        
        with pytest.raises(Exception):
            temporal_filter.operator = 123  # Should fail - not str
