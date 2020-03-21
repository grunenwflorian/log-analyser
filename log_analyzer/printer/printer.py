import json
from json import JSONEncoder
from typing import Dict, Any

from log_analyzer.steps import Action, Reporter


class PrinterAction(Action):
    NAME = "PrintAction"

    def __init__(self, args: Dict[str, Any]):
        super().__init__(args)
        self.data = bool(args["data"]) if ("data" in args) else True
        self.report = bool(args["report"]) if ("report" in args) else True

    def process(self, data: Dict[str, Any], report):
        if self.data:
            print("Data : ", json.dumps(data, cls=DictEncoder), end="")
        if self.report:
            print("Temp Report : ", json.dumps(report, cls=DictEncoder))


class PrinterReporter(Reporter):
    NAME = "PrintReporter"

    def analyze(self, report):
        print("Report : ", json.dumps(report, cls=DictEncoder))


class DictEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__

