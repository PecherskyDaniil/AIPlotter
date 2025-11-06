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


# Тесты для SettingsModel
class TestSettingsModel:
    def test_settings_model_initialization(self):
        """Test SettingsModel initialization"""
        settings = SettingsModel()
        assert settings.superset_host is None
        assert settings.superset_port is None
        assert settings.superset_username is None
        assert settings.superset_password is None
        assert settings.image_directory == ""
    
    def test_settings_model_setters(self):
        """Test SettingsModel setters"""
        settings = SettingsModel()
        settings.superset_host = "localhost"
        settings.superset_port = 8080
        settings.superset_username = "admin"
        settings.superset_password = "secret"
        settings.image_directory = "/path/to/images"
        
        assert settings.superset_host == "localhost"
        assert settings.superset_port == 8080
        assert settings.superset_username == "admin"
        assert settings.superset_password == "secret"
        assert settings.image_directory == "/path/to/images"
    
    def test_settings_model_invalid_types(self):
        """Test SettingsModel with invalid types"""
        settings = SettingsModel()
        
        with pytest.raises(Exception):
            settings.superset_host = 123  # Should fail - not str
        
        with pytest.raises(Exception):
            settings.superset_port = "not_an_int"  # Should fail - not int
