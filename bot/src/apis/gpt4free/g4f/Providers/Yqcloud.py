import os
import time
from httpx import Client

from ..typing import sha256, Dict, get_type_hints


def _create_completion(model: str, messages: list, **kwargs):

    headers = {
        'authority': 'api.aichatos.cloud',
        'origin': 'https://chat9.yqcloud.top',
        'referer': 'https://chat9.yqcloud.top/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    json_data = {
        'prompt': 'internacional | %s' % messages[-1]['content'],
        'userId': f'#/chat/{int(time.time() * 1000)}',
        'network': True,
        'apikey': '',
        'system': '',
        'withoutContext': False,
    }

    with Client() as http_client:
        response = http_client.post('https://api.aichatos.cloud/api/generateStream', headers=headers, json=json_data, stream=True)
    for token in response.iter_bytes(chunk_size=2046):
        if b'always respond in english' not in token:
            yield token.decode('utf-8')

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])