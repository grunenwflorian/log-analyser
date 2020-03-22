import argparse
import logging

from log_analyzer.analyzer.log_analyzer import LogAnalyzer
from log_analyzer.console.console import ConsoleReporter
from log_analyzer.csv.csv import CsvReporter
from log_analyzer.parser.log4j2_parser import Log4j2Parser
from log_analyzer.printer.printer import PrinterAction, PrinterReporter
from log_analyzer.provider import FileProvider
from log_analyzer.pipeline import ActionsReifier, ActionsExecutor


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
            {"name": Log4j2Parser.NAME},
            {"name": LogAnalyzer.NAME},
            {"name": PrinterAction.NAME, "data": False, "report": False}
        ],
        "reporters": [
            #{"name": PrinterReporter.NAME},
            {"name": ConsoleReporter.NAME},
            {"name": CsvReporter.NAME},
        ]
    })

    ActionsExecutor(models).execute()
