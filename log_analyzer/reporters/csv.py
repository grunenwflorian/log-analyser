import csv

from log_analyzer.steps import Reporter


def create_parser_row(opts):
    line_viewed = opts["all_lines"]
    parsed_line = opts["parsed_lines"]
    percent_viewed = (parsed_line / line_viewed) * 100
    return [line_viewed, parsed_line, percent_viewed]


def create_analyzer_global_row(parser_opts):
    return [
        parser_opts.info,
        parser_opts.debug,
        parser_opts.warn,
        parser_opts.error
    ]


def create_log_thread_report(analyzer):
    nb_logger = len(analyzer.log.keys())
    nb_thread = len(analyzer.thread.keys())
    return nb_logger, nb_thread


class CsvReporter(Reporter):
    NAME = "CsvReporter"

    def analyze(self, report):

        with open('stats.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            row = []
            if "parser" in report:
                row += create_parser_row(report["parser"])

            if "analyzer" in report:
                analyzer = report["analyzer"]
                row += create_analyzer_global_row(analyzer.glob)
                row += create_log_thread_report(analyzer)

            writer.writerow(row)
