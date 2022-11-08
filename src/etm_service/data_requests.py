import yaml

from .single_request import SingleRequest

class DataRequests:
    def __init__(self, single_requests):
        self.data_requests = single_requests

    def all(self):
        '''Generates all requests for parsing'''
        yield from self.data_requests

    def ready(self, batches):
        '''Sort the Values from the requests in batches for the endpoints'''
        for single_request in self.all():
            for value in single_request.values():
                batches.add(value)

    def combine(self, combiner):
        '''Use the combiner to inject the holon outcomes into the (SET) requests'''
        for single_request in self.all():
            combiner.inject(single_request)

    def convert(self):
        '''Start converters on all single_requests'''
        for request in self.all():
            request.calculate()

    def write_to(self, path):
        '''Tell all single requests to start writing their data'''
        for request in self.all():
            request.write_to(path)

    def to_dict(self):
        '''Returns the results as a dictionary (only available after calculation)'''
        return {result.key: result.value() for result in self.all()}

    @classmethod
    def load_from_path(cls, path, action='GET'):
        '''Loads the data requests from the config'''
        with open(path, 'r') as f:
            doc = yaml.load(f, Loader=yaml.FullLoader)

        return cls([SingleRequest(key, action, **data) for key, data in doc.items()])
