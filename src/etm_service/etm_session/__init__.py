from .copy import ETMCopySession
from .inputs import ETMGetInputsSession, ETMSetInputsSession
from .queries import ETMQuerySession
from .curves import ETMSetCurvesSession
from .nodes import ETMNodesSession
from .session import ETMSession

class ETMConnection:
    def __init__(self, endpoint_key, scenario_id, action='GET'):
        '''Connect to the endpoint named by the key'''
        self.action = action
        self.session = endpoint_key
        self.scenario_id = scenario_id

    @property
    def session(self):
        return self._session

    @session.getter
    def session(self):
        self._session.scenario_id = self.scenario_id
        return self._session

    @session.setter
    def session(self, endpoint_key):
        '''
        Sets the correct session based on the endpoint_key, if unavailable for this action
        returns an empty session
        TODO: or raise the invalid endpoint??
        '''
        if endpoint_key == 'queries':
            self._session = ETMQuerySession() if self.action == 'GET' else ETMSession()
        elif endpoint_key == 'curves':
            self._session = ETMSession() if self.action == 'GET' else ETMSetCurvesSession()
        elif endpoint_key == 'nodes':
            self._session = ETMNodesSession() if self.action == 'GET' else ETMSession()
        elif endpoint_key == 'inputs':
            self._session = ETMGetInputsSession() if self.action == 'GET' else ETMSetInputsSession()
        elif endpoint_key == 'copy':
            self._session = ETMCopySession()
        else:
            raise InvalidEndpoint(endpoint_key)

    def connect(self, requested_keys):
        '''
        Connect to the ETM through the ETMSession session, and yield the results
        of the response.

        Params:
            requested_keys(List[str]): A list of keys to request to the endpoint

        Returns:
            Generator[(str, float)] of results (key value pairs)
        '''
        yield from self.session.send_request(requested_keys)


class InvalidEndpoint(Exception):
    def __init__(self, endpoint, *args):
        mess = f'No method available to connect to endpoint {endpoint}'
        super().__init__(mess, *args)
