import json
from json import JSONEncoder
from typing import Dict, Any

from log_analyzer.steps import Action


class PrinterAction(Action):
    NAME = "PrintAction"

    def __init__(self, args: Dict[str, Any]):
        super().__init__(args)
        self.data = bool(args["data"]) if ("data" in args) else True
        self.report = bool(args["report"]) if ("report" in args) else True
        self.log = bool(args["log"]) if ("log" in args) else False

    def process(self, data: Dict[str, Any], report):
        if self.data:
            print("Data : ", json.dumps(data, cls=DictEncoder), end="")
        if self.report:
            print("Temp Report : ", json.dumps(report, cls=DictEncoder))
        if self.log:
            print(data["provider"])


class DictEncoder(JSONEncoder):

    def default(self, o):  # pylint: disable=method-hidden
        return o.__dict__
