from src.zzz_assistant.core.device import Device


class BaseTask:
    """
    所有任务的基类

    它不实现任何具体功能，但定义了所有“子任务”都必须拥有的东西：
    1. 一个 `__init__` 方法，用于接收共享的工具（如device, config）。
    2. 一个 `run` 方法的框架，所有子任务都需要去具体实现这个方法。
    """

    def __init__(self, device: Device, config: dict):
        """
        初始化任务

        :param device: 已经连接好的设备控制器对象
        :param config: 从yaml加载的全局配置字典
        """
        self.device = device
        self.config = config

    def run(self):
        """
        执行任务的入口
        这是一个“抽象方法”，子类必须重写（override）它，提供具体的实现。
        """

        # 使用 raise NotImplementedError 是一个标准的Python实践，
        # 它强制要求任何继承自 BaseTask 的子类都必须自己实现 run 方法，
        # 否则在调用时就会直接报错，提醒开发者“你忘了写具体逻辑了！”

        raise NotImplementedError("每个任务子类都必须实现自己的'run'方法")