import argparse

from log_analyzer.actions.csv import CsvSaver
from log_analyzer.pipeline import ActionsReifier, ActionsExecutor
from log_analyzer.provider.url import UrlProvider

from log_analyzer.reporters.console import ConsoleReporter
from log_analyzer.reporters.csv import CsvReporter

from log_analyzer.actions.analyzer.log import LogAnalyzer
from log_analyzer.actions.parser.grok import GrokParser
from log_analyzer.actions.printer import PrinterAction


def create_argument_parser():
    parser = argparse.ArgumentParser(description="parse incoming text")

    parser.add_argument("-f", "--file",
                        help="Path or URL to the file containing the files to analyze")
    parser.add_argument("-a", "--actions",
                        help="Generic steps to take on the different files separated by commas",
                        default="")
    return parser


if __name__ == "__main__":
    cmdline_args = create_argument_parser().parse_args()

    args = vars(cmdline_args)

    bff_patterns = [
        r"%{INT:year}-%{INT:month}-%{INT:day} %{HOUR:hour}:%{MINUTE:minute}:%{SECOND:second},%{INT:milli} \[%{DATA:thread}\] %{WORD:level}\s{1,2}%{DATA:log_name} - %{GREEDYDATA:message}",
        r"%{INT:year}-%{INT:month}-%{INT:day} %{HOUR:hour}:%{MINUTE:minute}:%{SECOND:second} %{WORD:level}\s{1,2}%{DATA:log_name} %{IP:ip} - %{GREEDYDATA:message}"
    ]

    models = ActionsReifier().reify_model({
        "provider": {"name": UrlProvider.NAME, "url": "https://macpro.fr.murex.com/ci/job/kubypop-deploy/job/2020_03_19-15_17_06-36606883/1646/artifact/kubypop/logs/kube_bff.log"},
        "actions": [
            {"name": GrokParser.NAME, "patterns": bff_patterns},
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
