from .batch import Batch

class Batches:
    def __init__(self, action='GET'):
        self._curves = Batch('curves', action)
        self._nodes = Batch('nodes', action)
        self._queries = Batch('queries', action)
        self._inputs = Batch('inputs', action)

    def each(self):
        yield self._curves
        yield self._nodes
        yield self._queries
        yield self._inputs

    def add(self, value):
        '''Adds a Value to the correct Batch'''
        if value.endpoint == 'curve':
            self._curves.add(value)
        elif value.endpoint == 'query':
            self._queries.add(value)
        elif value.endpoint == 'node_property':
            self._nodes.add(value)
        elif value.endpoint == 'input':
            self._inputs.add(value)
        else:
            raise UnknownValueType(f'{value} could not be added to a batch')

    def send(self, scenario_id):
        '''Sends all the batches'''
        for batch in self.each():
            batch.send(scenario_id)

class UnknownValueType(Exception):
    pass
