from log_analyzer.actions.csv import CsvSaver
from log_analyzer.provider.file import FileProvider

from log_analyzer.actions.analyzer.log import LogAnalyzer
from log_analyzer.actions.parser.grok import GrokParser
from log_analyzer.actions.printer import PrinterAction
from log_analyzer.provider.url import UrlProvider

from log_analyzer.reporters.csv import CsvReporter
from log_analyzer.reporters.console import ConsoleReporter
from log_analyzer.reporters.printer import PrinterReporter


class ActionsExecutor:

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


class Model:

    def __init__(self):
        self.provider = None
        self.actions = []
        self.reporters = []

    def set_provider(self, provider):
        self.provider = provider

    def add_action(self, action):
        self.actions.append(action)

    def add_reporter(self, reporter):
        self.reporters.append(reporter)


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

        self._reify_provider(args, models)

        if "actions" not in args:
            return models
        self._reify_model_actions(args, models)

        if "reporters" not in args:
            return models
        self._reify_model_reporters(args, models)

        return models

    def _reify_provider(self, args, model: Model):
        args_provider = args["provider"]
        provider_name = args_provider["name"]
        if provider_name not in self._providers:
            raise ValueError("No provider associated with the name " + provider_name)
        provider = self._providers[provider_name]
        model.set_provider(provider(args_provider))

    def _reify_model_actions(self, args, model: Model):
        user_actions = args["actions"]
        for action_conf in user_actions:
            action_name = action_conf["name"]
            if action_name not in self._actions:
                raise ValueError("No action_conf associated with the name " + action_name)
            action = self._actions[action_name](action_conf)
            model.add_action(action)

    def _reify_model_reporters(self, args, model: Model):
        user_reporters = args["reporters"]
        for reporter_conf in user_reporters:
            reporter_name = reporter_conf["name"]
            if reporter_name not in self._reporters:
                raise ValueError("No reporter_conf associated with the name " + reporter_name)
            reporter = self._reporters[reporter_name](reporter_conf)
            model.add_reporter(reporter)


def _init_default_provider():
    return {
        FileProvider.NAME: FileProvider,
        UrlProvider.NAME: UrlProvider
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
