from requests import Response

from .util import multi_fetch_json


class Scrapable(object):

    def __init__(self):
        pass

    def has_next_url(self) -> bool:
        return False

    def gen_url(self):
        return f'https://example.com/'

    def gen_url_params(self):
        return {}

    def verify(self, data: Response):
        return True

    def post_process(self, data: Response):
        pass

    def scrap(self):
        multi_fetch_json(
            self.gen_url,
            self.gen_url_params,
            self.has_next_url,
            self.post_process,
            self.verify
        )