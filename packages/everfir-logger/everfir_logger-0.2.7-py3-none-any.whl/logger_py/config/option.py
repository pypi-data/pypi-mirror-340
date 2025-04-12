import os
from typing import Callable

from logger_py.config.log_config import LogConfig
from logger_py.config.log_config import LOG_LEVEL

Option = Callable[[LogConfig], None]


def WithLogLevel(level: LOG_LEVEL) -> Option:
    return lambda config: setattr(config, "level", level)


def WithLogFile(file: str) -> Option:
    if not os.path.isabs(file):
        file = os.path.abspath(file)
    return lambda config: setattr(config, "log_file", file)


def WithLogRotation(rotation: bool) -> Option:
    return lambda config: setattr(config, "rotation", rotation)


def WithLogRotationInterval(interval: int) -> Option:
    return lambda config: setattr(config, "rotation_interval", interval)


def WithCaller(enable: bool, keep_level: int = 3) -> Option:
    def handler(config: LogConfig) -> None:
        setattr(config, "enable_caller", enable)
        setattr(config, "caller_keep_level", keep_level)

    return handler


def WithTracer(enable: bool) -> Option:
    return lambda config: setattr(config.tracer_config, "enable", enable)
