import requests

from .session import ETMSession

class ETMGetInputsSession(ETMSession):
    ENDPOINT = '/inputs'

    def send_request(self, keys):
        yield from self._handle_response(requests.get(self.url()), keys)

    def _handle_response(self, response, keys):
        if response.ok:
            data = response.json()
            return ((key, self._value_for(data[key])) for key in keys)

        return super()._handle_response(response)

    def _value_for(self, input):
        try:
            return input['user']
        except KeyError:
            return input['default']


class ETMSetInputsSession(ETMSession):
    ENDPOINT = '/'

    def send_request(self, data):
        json = {'scenario': {'user_values': data}}
        self._handle_response(requests.put(self.url(), json=json))
        yield True

    def _handle_response(self, response):
        if response.ok:
            return

        return super()._handle_response(response)
