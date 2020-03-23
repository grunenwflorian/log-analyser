import operator

from terminaltables import AsciiTable
from colorclass import Color

from log_analyzer.steps import Reporter


def redify(elem):
    return Color("{red}" + str(elem) + "{/red}")


def blueify(elem):
    return Color("{blue}" + str(elem) + "{/blue}")


def yellowify(elem):
    return Color("{yellow}" + str(elem) + "{/yellow}")


def greenify(elem):
    return Color("{green}" + str(elem) + "{/green}")


def report_parser(opts):
    line_viewed = opts["all_lines"]
    parsed_line = opts["parsed_lines"]
    percent_viewed = (parsed_line / line_viewed) * 100
    return "Nb Lines analyzed: " + greenify(parsed_line) + \
           ", Nb Lines viewed: " + redify(line_viewed) + \
           ", Percent analyzed : " + blueify(percent_viewed)


def percent(val, all_val):
    return (val / all_val) * 100


def report_analyzer_global(parser_opts, glob):
    all_lines = parser_opts["all_lines"]
    parsed_lines = parser_opts["parsed_lines"]
    info, warn, debug, error = glob.info, glob.warn, glob.debug, glob.error
    table_data = [
        ["Level", "Np", "Percent/analyzed", "Percent/viewed"],
        ["Info", info, percent(info, parsed_lines), percent(info, all_lines)],
        [yellowify("Warn"), warn, percent(warn, parsed_lines), percent(warn, all_lines)],
        ["Debug", debug, percent(debug, parsed_lines), percent(debug, all_lines)],
        [redify("Error"), error, percent(error, parsed_lines), percent(error, all_lines)]
    ]
    return table_data


def report_analyzer_level(level_meta):
    table_data = []
    for log, value in level_meta.items():
        colored_log = log

        if value.warn > 0:
            colored_log = yellowify(log)

        if value.error > 0:
            colored_log = redify(log)

        table_data.append([colored_log, value.info, value.warn, value.debug, value.error])

    table_data.sort(key=operator.itemgetter(4, 2, 1, 3), reverse=True)

    table_data.insert(0, ["Logger Name", "Info", "Warn", "Debug", "Error"])
    return table_data


class ConsoleReporter(Reporter):
    NAME = "Console"

    def analyze(self, report):
        if "parser" in report:
            print(report_parser(report["parser"]))

        if "analyzer" in report:
            # analyzer without parser not allowed
            parser = report["parser"]
            analyzer = report["analyzer"]
            global_table = AsciiTable(report_analyzer_global(parser, analyzer.glob))
            print(global_table.table)

            log_levels_table = report_analyzer_level(analyzer.log)
            print("Nb of loggers used: ", blueify(len(log_levels_table) - 1))
            log_table = AsciiTable(log_levels_table)
            print(log_table.table)

            thread_level_table = report_analyzer_level(analyzer.thread)
            print("Nb of thread that logged: ", blueify(len(thread_level_table) - 1))
            thread_table = AsciiTable(thread_level_table)
            print(thread_table.table)
