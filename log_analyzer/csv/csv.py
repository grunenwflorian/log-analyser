import csv

from log_analyzer.steps import Reporter


def create_parser_row(opts):
    line_viewed = opts["line_viewed"]
    parsed_line = opts["parsed_line"]
    percent_viewed = (parsed_line / line_viewed) * 100
    return [line_viewed, parsed_line, percent_viewed]


def create_analyzer_global_row(parser_opts):
    return [
        parser_opts.info,
        parser_opts.debug,
        parser_opts.warn,
        parser_opts.error
    ]


class CsvReporter(Reporter):
    NAME = "CsvReporter"

    def analyze(self, report):
        with open('stats.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            row = []
            if "parser" in report:
                parser_csv = create_parser_row(report["parser"])
                row += parser_csv

            if "analyzer" in report:
                analyzer = report["analyzer"]
                global_meta_csv = create_analyzer_global_row(analyzer.meta_global)
                row += global_meta_csv

                nb_logger = len(analyzer.log_meta.keys())
                nb_thread = len(analyzer.thread_meta.keys())
                row += [nb_logger, nb_thread]

            spamwriter.writerow(row)
