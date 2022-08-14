import typing
import requests


class VerifyError(Exception):
    pass


def multi_fetch_json(
        url_generator: typing.Callable[[], str],
        url_param: typing.Callable[[], typing.Dict],
        has_next_url: typing.Callable[[], bool],
        post_process: typing.Callable[[typing.Any], typing.Any],
        verify: typing.Callable[[typing.Any], bool] = (lambda data: True),
):

    while has_next_url():
        _url = url_generator()
        _url_params = url_param()
        with requests.get(_url, params=_url_params) as resp:
            if not verify(resp):
                raise VerifyError(f'Verification failed for url {_url}')
            post_process(resp)
