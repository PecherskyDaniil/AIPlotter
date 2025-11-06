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

# Интеграционные тесты
class TestIntegration:
    def test_complete_dashboard_creation(self):
        """Test creating a complete dashboard with all components"""
        # Create datasource
        datasource = DatasourceModel()
        datasource.name = "Test DB"
        datasource.datasource_id = 1
        datasource.datasource_type = "sqlite"
        
        # Create columns
        column1 = ColumnModel()
        column1.name = "sales"
        column1.column_id = 1
        
        column2 = ColumnModel()
        column2.name = "category"
        column2.column_id = 2
        
        # Create metrics
        metric1 = MetricModel()
        metric1.aggregate = "SUM"
        metric1.column = column1
        
        # Create filters
        filter1 = TemporalRangeFilterModel()
        filter1.subject = "date"
        filter1.comparator = "2024-01-01"
        
        # Create charts
        bar_chart = BarChartModel()
        bar_chart.name = "Sales Chart"
        bar_chart.x_axis = "category"
        bar_chart.metrics = [metric1]
        bar_chart.group_by = ["region"]
        bar_chart.datasource = datasource
        bar_chart.filters = [filter1]
        bar_chart.chart_id = 1
        
        pie_chart = PieChartModel()
        pie_chart.name = "Sales Pie"
        pie_chart.metrics = [metric1]
        pie_chart.group_by = ["category"]
        pie_chart.datasource = datasource
        pie_chart.chart_id = 2
        
        # Create dashboard
        dashboard = DashboardModel()
        dashboard.name = "Sales Dashboard"
        dashboard.charts = [bar_chart, pie_chart]
        
        # Assertions
        assert dashboard.name == "Sales Dashboard"
        assert len(dashboard.charts) == 2
        assert dashboard.charts[0].viz_type == VizType.BAR
        assert dashboard.charts[1].viz_type == VizType.PIE
        assert dashboard.charts[0].metrics[0].aggregate == "SUM"