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
        LEVEL_TO_LAMBDA[level](self.log_report.glob, parsed_logs)

        if "log_name" in parsed_logs:
            self._update_log_report(level, parsed_logs)

        if "thread" in parsed_logs:
            self._update_thread_report(level, parsed_logs)

        report["analyzer"] = self.log_report

    def _update_log_report(self, level, parsed_logs):
        log_name = parsed_logs["log_name"]
        if log_name not in self.log_report.log:
            self.log_report.add_logger(log_name, LevelReporter())
        log_reporter = self.log_report.logger_reporter(log_name)
        LEVEL_TO_LAMBDA[level](log_reporter, None)

    def _update_thread_report(self, level, parsed_logs):
        thread_name = parsed_logs["thread"]
        if thread_name not in self.log_report.thread:
            self.log_report.add_thread(thread_name, LevelReporter())
        thread_reporter = self.log_report.thread_reporter(thread_name)
        LEVEL_TO_LAMBDA[level](thread_reporter, None)


class LevelReporter:

    def __init__(self) -> None:
        self.info = 0
        self.warn = 0
        self.debug = 0
        self.error = 0
        self.meta_errors = []

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value


class Report:

    def __init__(self) -> None:
        self.glob = LevelReporter()
        self.log = {}
        self.thread = {}

    def add_logger(self, log_name, level_report: LevelReporter) -> None:
        self.log[log_name] = level_report

    def logger_reporter(self, log_name) -> LevelReporter:
        return self.log[log_name]

    def add_thread(self, thread_name, level_report: LevelReporter) -> None:
        self.thread[thread_name] = level_report

    def thread_reporter(self, thread_name) -> LevelReporter:
        return self.thread[thread_name]


def info(reporter, _):
    reporter.info += 1


def debug(reporter, _):
    reporter.debug += 1


def warn(reporter, _):
    reporter.warn += 1


def error(reporter, parsed_logs):
    reporter.error += 1
    if parsed_logs:
        date = parsed_logs["date"]
        message = parsed_logs["message"]
        reporter.meta_errors.append({"date": date, "message": message})


LEVEL_TO_LAMBDA = {
    "INFO": info,
    "DEBUG": debug,
    "WARN": warn,
    "ERROR": error
}
