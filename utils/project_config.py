import os
import yaml
from .argument_utils import ArgumentUtils

class ProjectConfig:
    """"
    项目配置类 单例模式
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._config = None
        self._args = None
    #初始化配置
    def initialize(self):
        """
        初始化配置
        :return:
        """
        if self._args is None:
            args_utils = ArgumentUtils()
            self._args = args_utils.parse_args()
        if self._config is None:
            config = self._load_yaml(self._args.config)
            private_config = self._load_yaml("config.private.yaml")
            config.update(private_config)

        overridden = {}
        for key, value in vars(self._args).items():#vars()函数返回当前作用域的变量字典
           if key in config and value is not None:
                overridden[key] = value
        config.update(overridden)
        self._normalize_bool(config, "memory_enabled")
        self._normalize_bool(config, "resume_from_checkpoint")
        config["apikey"] = self._resolve_api_key(config.get("apikey"))
        self._config = config

    def _load_yaml(self, file_path):
        if not os.path.exists(file_path):
            return {}
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def _resolve_api_key(self, fallback):
        return (
            os.getenv("BOOKTRANSLATOR_API_KEY")
            or os.getenv("DEEPSEEK_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or fallback
        )

    def _normalize_bool(self, config, key):
        value = config.get(key)
        if isinstance(value, str):
            config[key] = value.lower() == "true"

    def __getattr__(self, item):
        """
        获取配置项
        :return:
        """
        if self._config and item in self._config:
            return self._config[item]
        else:
            raise AttributeError(f"配置项 {item} 不存在")



if __name__ == "__main__":
    # 测试单例模式
    p1 = ProjectConfig()
    p1.initialize()
