from typing import Dict, Any
from datetime import datetime

from pygrok import Grok

from log_analyzer.steps import Action


class GrokParser(Action):
    NAME = "Grok"

    def __init__(self, args: Dict[str, Any]):
        super().__init__(args)
        self.groks = list(map(Grok, args["patterns"]))
        self.report = {"all_lines": 0, "parsed_lines": 0}

    def process(self, data: Dict[str, Any], report):
        line = data["provider"]
        self.report["all_lines"] += 1

        for grok_parser in self.groks:
            parsed_log = grok_parser.match(line)

            if parsed_log:
                parsed_log["date"] = create_datetime(parsed_log)
                data["parser"] = parsed_log
                self.report["parsed_lines"] += 1
                break

        report["parser"] = self.report


def create_datetime(parsed_log):
    year = int(parsed_log["year"])
    month = int(parsed_log["month"])
    day = int(parsed_log["day"])
    hour = int(parsed_log["hour"])
    minute = int(parsed_log["minute"])
    second = int(parsed_log["second"])
    milli = 0
    if "milli" in parsed_log:
        milli = int(parsed_log["milli"])
    return datetime(year, month, day, hour, minute, second, milli)
