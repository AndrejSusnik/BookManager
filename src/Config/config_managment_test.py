from config_managment import CustomConfigManager

def test_create_custom_config_manager():
    config_manager = CustomConfigManager('./')
    assert config_manager is not None