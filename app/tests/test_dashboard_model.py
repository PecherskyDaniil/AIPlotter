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
# Тесты для DashboardModel
class TestDashboardModel:
    def test_dashboard_model_initialization(self):
        """Test DashboardModel initialization"""
        dashboard = DashboardModel()
        assert len(dashboard.name) == 32  # Random string length
        assert dashboard.charts == []
    
    def test_dashboard_model_charts_validation(self):
        """Test DashboardModel charts list validation"""
        dashboard = DashboardModel()
        
        # Valid charts
        valid_charts = [BarChartModel(), PieChartModel(), ScatterChartModel()]
        dashboard.charts = valid_charts
        assert dashboard.charts == valid_charts
        
        # Invalid charts
        with pytest.raises(Exception):
            dashboard.charts = [BarChartModel(), "not_a_chart"]
