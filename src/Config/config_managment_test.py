from config_managment import CustomConfigManager, EtcdConfig

def test_create_custom_config_manager():
    config_manager = CustomConfigManager('./')
    assert config_manager is not None

def test_etcd():
    config = EtcdConfig(host='localhost', port=4001)
    configman = CustomConfigManager('./', useEtcd=True, ectd_config=config)

    configman.get('DB_URL')