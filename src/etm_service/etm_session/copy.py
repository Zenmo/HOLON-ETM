import requests

from etm_service.config import Config
from .session import ETMSession

class ETMCopySession(ETMSession):
    '''Copies the ETM scenario and sets the new ID in the Config'''
    ENDPOINT = '/'

    def send_request(self, _):
        json = {'scenario': {'scenario_id': Config().scenario['id']}}
        self._handle_response(requests.post(self.url(), json=json))
        yield True

    def _handle_response(self, response):
        if response.ok:
            data = response.json()
            Config().scenario['id'] = data['id']
            return

        return super()._handle_response(response)
