import json
import pathlib

from requests import Response

from scrap.scrapable import Scrapable


class SteamReview(Scrapable):

    def __init__(self, app_id: int, write_path: pathlib.PurePath | str = None):
        super().__init__()
        self.app_id = app_id
        self.previous_cursor = ''
        self.current_cursor = '*'
        self.data: dict = {}
        self._count = 0
        self.write_path = pathlib.Path(write_path)
        if self.write_path:
            self.write_path.mkdir(parents=True, exist_ok=True)
            assert self.write_path.is_dir()

    def has_next_url(self) -> bool:
        return self.previous_cursor != self.data.get('cursor')
        # return True if self._count < 10 else False

    def gen_url(self):
        return f'https://store.steampowered.com/appreviews/{self.app_id}'

    def gen_url_params(self):
        return {
            'json': 1,
            'language': 'all',
            'filter': 'recent',
            'num_per_page': 100,
            'cursor': self.current_cursor
        }

    def verify(self, data: Response):
        data.raise_for_status()
        data = data.json()
        return data.get('success') and self.current_cursor != data.get('cursor')

    def post_process(self, data: Response):
        self._count += 1
        self.data = data.json()
        self.previous_cursor = self.current_cursor
        self.current_cursor = self.data['cursor']
        if self.write_path:
            file_path = pathlib.Path(self.write_path, str(self.app_id), f'{self._count}.json')
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w') as f:
                print(f'Write {file_path}')
                f.write(data.text)
        else:
            print(data)
