import requests

from etm_service.config import Config

class ETMSession:
    def __init__(self):
        pass

    @property
    def scenario_id(self):
        return self._scenario_id

    @scenario_id.setter
    def scenario_id(self, val):
        self._scenario_id = val

    @scenario_id.getter
    def scenario_id(self):
        if not self._scenario_id:
            return Config().scenario['id']

        return self._scenario_id

    def send_request(self, data):
        '''Generator of Results'''
        yield from ()

    def url(self):
        return f"{Config().api_url}{self.scenario_id}{self.ENDPOINT}"

    def _handle_response(self, response: requests.Response):
        '''Return the handled response (list/dict of outcomes)'''
        if response.status_code == 422:
            self.fail_with(errors=response.json()['errors'])

        self.fail_with(f"Something went wrong connecting to the ETM, status_code: {response.status_code}, body: {response.text[:200]}")

    def fail_with(self, message='', errors=[]):
        if not message and errors:
            message = ', '.join(errors)
        raise ETMConnectionError(message)


class ETMConnectionError(BaseException):
    pass
