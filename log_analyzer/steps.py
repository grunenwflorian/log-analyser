from abc import abstractmethod
from enum import Enum
from typing import Any, Dict


class ActionType(Enum):
    PROVIDER = 0
    ACTIONS = 1
    POST_ACTIONS = 2


class Action:
    def __init__(self, args: Dict[str, Any]):
        self.name = args["name"]

    @abstractmethod
    def process(self, data: Dict[str, Any], report):
        pass

    def clean(self):
        pass


class Reporter:
    def __init__(self, args: Dict[str, Any]):
        self.name = args["name"]

    @abstractmethod
    def analyze(self, report):
        pass

    def clean(self):
        pass


class Provider:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass
