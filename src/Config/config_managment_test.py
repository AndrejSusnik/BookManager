from config_managment import CustomConfigManager, EtcdConfig
import etcd

def test_create_custom_config_manager():
    config_manager = CustomConfigManager('./')
    assert config_manager is not None

def test_etcd():
    config = EtcdConfig(host='localhost', port=2379)

    client = etcd.Client(host=config.host, port=config.port)
    client.write('/db/url', 'localhost')
    
    configman = CustomConfigManager(useEtcd=True, ectd_config=config)

    a = configman.get('DB_URL')
    client.delete('/db/url')

    assert a == 'localhost'

if __name__ == "__main__":
    test_create_custom_config_manager()
    test_etcd()