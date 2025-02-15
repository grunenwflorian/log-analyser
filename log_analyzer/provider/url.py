import requests

from log_analyzer.steps import Provider


class UrlProvider(Provider):
    NAME = "Url"

    def __init__(self, args):
        super().__init__(args)
        self.url = args["url"]
        self.iter = None
        self.req = None

    def __iter__(self):
        self.req = requests.get(self.url, stream=True)
        self.iter = iter(self.req.iter_lines())
        return self

    def __next__(self):
        return str(next(self.iter), self.req.encoding)
