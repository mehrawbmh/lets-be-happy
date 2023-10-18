from enum import Enum


class EnvMode(str, Enum):
    TEST = 'test'
    PRODUCTION = 'production'
