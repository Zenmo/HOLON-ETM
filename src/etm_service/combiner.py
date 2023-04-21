from .converters import Empty
from .single_request import MissingRequestInfoException

class Combiner:
    '''
    Combine HOLON outcomes with the requests to the ETM
    Only cares about the intersection of requests and results,
    this means a lot of validation needs to be done by the user.
    '''

    def __init__(self, holon_outcomes):
        self.holon_outcomes = holon_outcomes

    def inject(self, single_request):
        '''
        Find HOLON outcome and inject into request
        Assumes this is always the main value
        '''
        match = self._match(single_request.key)
        if match:
            single_request.set_value(match)

    def _match(self, key) -> float:
        '''Returns the value of the match if there is one,'''
        for holon_key, value in self.holon_outcomes.items():
            if key == holon_key:
                return value

class RequestsToOne:
    """
    Set the values of all requests to 1, to ready for the conversion steps
    when setting inputs on a scenario
    """

    @staticmethod
    def inject(single_request):
        if isinstance(single_request.converter, Empty):
            raise MissingRequestInfoException(
                f"Setting {single_request.key}: on SET action conversions can't be blank"
            )

        single_request.set_value(1.0)
