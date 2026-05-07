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
            with open(self._args.config, 'r') as f:
                config = yaml.safe_load(f)
                # print(config)
        overridden={}
        for key, value in vars(self._args).items():#vars()函数返回当前作用域的变量字典
            # print(key, value)
           if key in config and value is not None:
                overridden[key] = value
        config.update(overridden)
        # print(config)
        self._config = config
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

