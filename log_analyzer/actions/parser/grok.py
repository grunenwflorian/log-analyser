from typing import Dict, Any
from pygrok import Grok
from datetime import datetime

from log_analyzer.steps import Action


class GrokParser(Action):
    NAME = "Grok"

    def __init__(self, name):
        super().__init__(name)
        patterns = [
            "%{INT:year}-%{INT:month}-%{INT:day} %{HOUR:hour}:%{MINUTE:minute}:%{SECOND:second},%{INT:milli} \[%{DATA:thread}\] %{WORD:level}\s{1,2}%{DATA:log_name} - %{GREEDYDATA:message}",
            "%{INT:year}-%{INT:month}-%{INT:day} %{HOUR:hour}:%{MINUTE:minute}:%{SECOND:second} %{WORD:level}\s{1,2}%{DATA:log_name} %{IP:ip} - %{GREEDYDATA:message}"
        ]
        self.groks = list(map(lambda pattern: Grok(pattern), patterns))
        self.report = {"line_viewed": 0, "parsed_line": 0}

    def process(self, data: Dict[str, Any], report):
        line = data["provider"]

        self.report["line_viewed"] += 1
        for grok in self.groks:
            parsed_log = grok.match(line)

            if parsed_log:
                parsed_log["date"] = self.create_datetime(parsed_log)
                data["parser"] = parsed_log
                self.report["parsed_line"] += 1
                break

        report["parser"] = self.report

    def create_datetime(self, parsed_log):
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


if __name__ == "__main__":
    "%d{yyyy-MM-dd HH:mm:ss,SSS} [%t] %-5level %logger{36} - %msg%n"
    logs = "2020-03-21 10:54:13 INFO  RequestLog:qtp2129221032-26: 10.244.9.13 - - [21/Mar/2020:10:54:13 +0000] \"GET /v1/bi/dashboards/dashboards/10179/views/15968 HTTP/1.1\" 304 0"
    pattern2 = "%{INT:year}-%{INT:month}-%{INT:day} %{HOUR:hour}:%{MINUTE:minute}:%{SECOND:second} %{WORD:level}\s{1,2}%{DATA:log_name} %{IP:ip} - %{GREEDYDATA:message}"
    grok = Grok(pattern2)
    print(grok.match(logs))
