import argparse
import logging

from log_analyzer.actions.csv import CsvSaver
from log_analyzer.pipeline import ActionsReifier, ActionsExecutor

from log_analyzer.reporters.console import ConsoleReporter
from log_analyzer.reporters.csv import CsvReporter

from log_analyzer.actions.analyzer.log import LogAnalyzer
from log_analyzer.actions.parser.grok import GrokParser
from log_analyzer.actions.printer import PrinterAction

from log_analyzer.provider.file import FileProvider


logger = logging.getLogger(__name__)


def create_argument_parser():
    parser = argparse.ArgumentParser(description="parse incoming text")

    parser.add_argument("-f", "--file",
                        help="Path to the file or dir containing the files to analyze")
    parser.add_argument("-a", "--actions",
                        help="Generic steps to take on the different files separated by commas",
                        default="")
    return parser


if __name__ == "__main__":
    cmdline_args = create_argument_parser().parse_args()

    args = vars(cmdline_args)

    models = ActionsReifier().reify_model({
        "provider": {"name": FileProvider.NAME, "path": args["file"]},
        "actions": [
            {"name": GrokParser.NAME},
            {"name": LogAnalyzer.NAME},
            {"name": CsvSaver.NAME},
            {"name": PrinterAction.NAME, "data": False, "report": False}
        ],
        "reporters": [
            # {"name": PrinterReporter.NAME},
            {"name": ConsoleReporter.NAME},
            {"name": CsvReporter.NAME},
        ]
    })

    ActionsExecutor(models).execute()
