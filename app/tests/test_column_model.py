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


class TestColumnModel:
    def test_column_model_initialization(self):
        """Test ColumnModel initialization with default values"""
        column = ColumnModel()
        assert column.name is None
        assert column.column_id is None
        assert column.json is None
    
    def test_column_model_setters_valid_types(self):
        """Test ColumnModel setters with valid types"""
        column = ColumnModel()
        column.name = "test_column"
        column.column_id = 123
        column.json = {"key": "value"}
        
        assert column.name == "test_column"
        assert column.column_id == 123
        assert column.json == {"key": "value"}
    
    def test_column_model_setters_invalid_types(self):
        """Test ColumnModel setters with invalid types"""
        column = ColumnModel()
        
        with pytest.raises(Exception):
            column.name = 123  # Should fail - not str
        
        with pytest.raises(Exception):
            column.column_id = "not_an_int"  # Should fail - not int
        
        with pytest.raises(Exception):
            column.json = "not_a_dict"  # Should fail - not dict


