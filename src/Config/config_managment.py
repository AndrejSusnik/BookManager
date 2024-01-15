from typing import List, Callable, Any
import dotenv
import yaml
import json
import os

class CustomConfigManager:
    def __init__(self, path: str) -> None:
        self.path = path
        self.load_configurations()
        self.callbacks: List[Callable[[Any], None]] = []

    def load_configurations(self):
        # precedence: default > env > dotenv > yaml > config_server
        
        # load environment variables from .env file
        self.dotenv_variables = dotenv.dotenv_values()

        self.env_variables = os.environb

        # load config.yml file
        with open(self.path + 'config.yaml') as f:
            self.yaml_variables = self.__parse_yaml(yaml.load(f, Loader=yaml.FullLoader))

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

    def get(self, key: str, for_service: str="", default: str="") -> str:
        if key in self.yaml_variables:
            return self.yaml_variables[key]
        elif key in self.dotenv_variables:
            return self.dotenv_variables[key]
        elif key in self.env_variables:
            return self.env_variables[key]

        return default

if __name__ == "__main__":
    config = CustomConfigManager("./")