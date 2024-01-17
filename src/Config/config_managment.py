from typing import List, Callable, Any
import dotenv
import yaml
import json
from typing import Optional
import os
import etcd

class EtcdConfig:
    def __init__(self, host='localhost', port=4001) -> None:
        self.host = host
        self.port = port

class CustomConfigManager:
    def __init__(self, path: str='./', useEtcd: bool=False, ectd_config: Optional[EtcdConfig]=None) -> None:
        self.path = path
        self.has_etcd_error = False
        if useEtcd and (ectd_config is None):
            raise Exception("EtcdConfig is required when useEtcd is True")
        elif useEtcd and (ectd_config is not None):
            try:
                self.etcd_client = etcd.Client(host=ectd_config.host, port=ectd_config.port) if useEtcd else None
                if self.etcd_client is not None:
                    self.useEtcd = True
                else:
                    self.useEtcd = False
            except Exception:
                self.has_etcd_error = True
                self.etcd_client = None
                self.useEtcd = False
                # raise Exception("Could not connect to etcd server")
        else:
            self.etcd_client = None
            self.useEtcd = False

            
        self.load_configurations()
        self.callbacks: List[Callable[[Any], None]] = []

    def load_configurations(self):
        # precedence: default < env < dotenv < yaml < config_server
        
        # load environment variables from .env file
        self.dotenv_variables = dotenv.dotenv_values()

        self.env_variables = os.environ

        # load config.yml file
        try:
            with open(self.path + 'config.yaml') as f:
                self.yaml_variables = self.__parse_yaml(yaml.load(f, Loader=yaml.FullLoader))
        except FileNotFoundError:
            self.yaml_variables = {}

    def __parse_yaml(self, yaml: dict[str, str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for key, value in yaml.items():
            if isinstance(value, dict):
                for sub_key, sub_value in self.__parse_yaml(value).items():
                    result[key + "_" + sub_key] = sub_value
            else:
                result[key] = value

        # turn all keys to uppercase
        return {key.upper(): value for key, value in result.items()}

    def reload_configurations(self):
        self.load_configurations()
        self.notify_change()

    def notify_change(self):
        for callback in self.callbacks:
            callback(self)

    def register_callback(self, callback: Callable[[Any], None]):
        self.callbacks.append(callback)

    def unregister_callback(self, callback: Callable[[Any], None]):
        self.callbacks.remove(callback)

    def _get_etcd_path(self, key: str, for_service: str="") -> str:
        return ''.join(list(map(lambda x: '/' if x == '_' else x, key.lower())))

    def check_etcd(self, key: str, for_service: str="") -> bool:
        try:
            val = self.etcd_client.read(self._get_etcd_path(key, for_service)).value
            return True, val
        except etcd.EtcdKeyNotFound:
            return False, None

    def get(self, key: str, for_service: str="", default: str="") -> str:
        if self.useEtcd and not self.has_etcd_error and self.etcd_client is not None:
            found, val =  self.check_etcd(key, for_service)
            if found and val is not None:
                return val

        if key in self.yaml_variables:
            return self.yaml_variables[key]
        elif key in self.dotenv_variables:
            return self.dotenv_variables[key]
        elif key in self.env_variables:
            return self.env_variables[key]

        return default

if __name__ == "__main__":
    config = CustomConfigManager("./")