from json import JSONEncoder, dumps

from log_analyzer.steps import Reporter


class PrinterReporter(Reporter):
    NAME = "PrintReporter"

    def analyze(self, report):
        print("Report : ", dumps(report, cls=DictEncoder))


class DictEncoder(JSONEncoder):

    def default(self, o):
        return o.__dict__

