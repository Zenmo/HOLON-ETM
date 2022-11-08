import requests

from etm_service.config import Config
from .session import ETMSession

class ETMCopySession(ETMSession):
    '''Copies the ETM scenario and sets the new ID in the Config'''
    ENDPOINT = '/'

    def send_request(self, scenario_id):
        json = {'scenario': {'scenario_id': scenario_id}}
        yield self._handle_response(requests.post(Config().api_url, json=json))

    def _handle_response(self, response):
        if response.ok:
            return response.json()['id']

        return super()._handle_response(response)
