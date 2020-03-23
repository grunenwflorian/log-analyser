from log_analyzer.actions.csv import CsvSaver
from log_analyzer.provider.file import FileProvider

from log_analyzer.actions.analyzer.log import LogAnalyzer
from log_analyzer.actions.parser.grok import GrokParser
from log_analyzer.actions.printer import PrinterAction

from log_analyzer.reporters.csv import CsvReporter
from log_analyzer.reporters.console import ConsoleReporter
from log_analyzer.reporters.printer import PrinterReporter


class ActionsExecutor(object):

    def __init__(self, models):
        self.provider = models.provider
        self.actions = models.actions
        self.reporters = models.reporters

    def execute(self):
        report = {}

        for line in self.provider:
            self._process_actions(line, report)

        for action in self.actions:
            action.clean()

        for reporter in self.reporters:
            reporter.analyze(report)

    def _process_actions(self, line, report):
        data = {"provider": line}
        for action in self.actions:
            action.process(data, report)


class Model(object):

    def __init__(self):
        self.provider = None
        self.actions = []
        self.reporters = []


class ActionsReifier:

    def __init__(self):
        self._providers = _init_default_provider()
        self._actions = _init_default_actions()
        self._reporters = _init_default_reporters()

    def add_provider(self, provider):
        self._providers = provider

    def add_action(self, name, action):
        self._actions[name] = action

    def add_reporter(self, name, reporter):
        self._reporters[name] = reporter

    def reify_model(self, args):
        models = Model()
        if "provider" not in args:
            raise ValueError("No data provider were provided")

        args_provider = args["provider"]
        provider_name = args_provider["name"]
        if provider_name not in self._providers:
            raise ValueError("No provider associated with the name " + provider_name)
        provider = self._providers[provider_name]
        models.provider = provider(args_provider)

        if "actions" not in args:
            # TODO handle validation
            return models
        user_actions = args["actions"]

        for action in user_actions:
            action_name = action["name"]
            if action_name not in self._actions:
                raise ValueError("No action associated with the name " + action_name)
            _action = self._actions[action_name](action)
            models.actions.append(_action)

        if "reporters" not in args:
            # TODO handle validation
            return models
        user_reporters = args["reporters"]

        for reporter in user_reporters:
            reporter_name = reporter["name"]
            if reporter_name not in self._reporters:
                raise ValueError("No reporter associated with the name " + reporter_name)
            _reporter = self._reporters[reporter_name](reporter)
            models.reporters.append(_reporter)

        return models


def _init_default_provider():
    return {
        FileProvider.NAME: FileProvider
    }


def _init_default_actions():
    return {
        PrinterAction.NAME: PrinterAction,
        GrokParser.NAME: GrokParser,
        LogAnalyzer.NAME: LogAnalyzer,
        CsvSaver.NAME: CsvSaver
    }


def _init_default_reporters():
    return {
        PrinterReporter.NAME: PrinterReporter,
        ConsoleReporter.NAME: ConsoleReporter,
        CsvReporter.NAME: CsvReporter
    }
