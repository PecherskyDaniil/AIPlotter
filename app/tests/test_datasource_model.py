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

# Тесты для DatasourceModel
class TestDatasourceModel:
    def test_datasource_model_initialization(self):
        """Test DatasourceModel initialization"""
        datasource = DatasourceModel()
        assert datasource.name is None
        assert datasource.datasource_id is None
        assert datasource.datasource_type is None
    
    def test_datasource_model_setters(self):
        """Test DatasourceModel setters"""
        datasource = DatasourceModel()
        datasource.name = "test_datasource"
        datasource.datasource_id = 456
        datasource.datasource_type = "postgresql"
        
        assert datasource.name == "test_datasource"
        assert datasource.datasource_id == 456
        assert datasource.datasource_type == "postgresql"
