from typing import Dict, Any

from log_analyzer.steps import Action


class LogAnalyzer(Action):
    NAME = "LogAnalyzer"

    def __init__(self, args: Dict[str, Any]):
        super().__init__(args)
        self.log_report = Report()

    def process(self, data: Dict[str, Any], report):
        if "parser" not in data:
            return

        parsed_logs = data["parser"]

        level = parsed_logs["level"]
        levelToLambda[level](self.log_report.meta_global)

        log_name = parsed_logs["log_name"]
        if log_name not in self.log_report.log_meta:
            self.log_report.log_meta[log_name] = LevelReporter()
        log_meta = self.log_report.log_meta[log_name]
        levelToLambda[level](log_meta)

        if "thread" in parsed_logs:
            self._update_thread_report(level, parsed_logs)

        report["analyzer"] = self.log_report

    def _update_thread_report(self, level, parsed_logs):
        thread_name = parsed_logs["thread"]
        if thread_name not in self.log_report.thread_meta:
            self.log_report.thread_meta[thread_name] = LevelReporter()
        thread_meta = self.log_report.thread_meta[thread_name]
        levelToLambda[level](thread_meta)


class Report(object):

    def __init__(self) -> None:
        self.meta_global = LevelReporter()
        self.log_meta = {}
        self.thread_meta = {}


class LevelReporter(object):

    def __init__(self) -> None:
        self.info = 0
        self.warn = 0
        self.debug = 0
        self.error = 0

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

def info(meta):
    meta.info += 1


def debug(meta):
    meta.debug += 1


def warn(meta):
    meta.warn += 1


def error(meta):
    meta.error += 1


levelToLambda = {
    "INFO": info,
    "DEBUG": debug,
    "WARN": warn,
    "ERROR": error
}

