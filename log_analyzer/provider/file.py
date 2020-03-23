from typing import Dict

from ..steps import Provider


class FileProvider(Provider):
    NAME = "File"

    def __init__(self, args: Dict[str, str]):
        super().__init__(FileProvider.NAME)
        self.path = args["path"]
        self.file = None
        self.iter = None

    def __iter__(self):
        self.file = open(self.path, "r")
        self.iter = iter(self.file)
        return self

    def __next__(self):
        try:
            return next(self.iter)
        except StopIteration:
            self.file.close()
            raise StopIteration
