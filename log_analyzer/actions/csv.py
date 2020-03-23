import csv
from typing import Dict, Any

from log_analyzer.steps import Action


class CsvSaver(Action):
    NAME = "CsvSaver"

    def __init__(self, args: Dict[str, Any]):
        super().__init__(args)
        file_name = args["file"] if "file" in args else "log_series.csv"
        self.csv_file = open(file_name, "w")
        self.writer = csv.writer(
            self.csv_file, delimiter=',')

    def process(self, data: Dict[str, Any], _):
        if "parser" not in data:
            return
        parser_data = data["parser"]
        self.writer.writerow([parser_data["level"], parser_data["date"].isoformat()])

    def clean(self):
        super().clean()
        self.csv_file.close()
