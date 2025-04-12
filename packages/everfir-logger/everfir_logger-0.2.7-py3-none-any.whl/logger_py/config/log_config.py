import logging
from enum import StrEnum
from logger_py.config.tracer_config import TracerConfig


# 日志等级
class LOG_LEVEL(StrEnum):
    DEBUG: str = logging._levelToName[logging.DEBUG]
    INFO: str = logging._levelToName[logging.INFO]
    WARN: str = logging._levelToName[logging.WARNING]
    ERROR: str = logging._levelToName[logging.ERROR]
    FATAL: str = logging._levelToName[logging.CRITICAL]


class LogConfig(object):

    def __init__(self):
        self.level: LOG_LEVEL = LOG_LEVEL.INFO  # 日志等级

        # 日志输出配置
        self.log_file: str = ""  # 日志输出路径
        self.rotation: bool = True
        self.compress: bool = False  # 日志压缩
        self.rotation_interval: int = 1  # 轮动时间间隔, 单位:小时

        # 日志内容
        self.enable_caller: bool = True  # 是否输出调用者信息
        self.caller_keep_level: int = 3  # 调用者信息保留的层级

        # TODO：链路追踪
        self.tracer_config: TracerConfig = TracerConfig()
        pass

    pass


_globalConfig = LogConfig()


def GetConfig() -> LogConfig:
    return _globalConfig
