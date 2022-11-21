from .converter import RequestConverter, MissingRequestInfoException
from etm_service.action import Action

class SingleRequest(RequestConverter, Action):
    def __init__(self, key, action, **config_data):
        self.key = key
        self.action = action
        self.converter = config_data

    def calculate(self):
        '''Run the converter of the request'''
        self.converter.calculate()

    def values(self):
        yield from self.converter.required_for_calculation()

    def write_to(self, path):
        self.converter.main_value.write_to(path / f'{self.key}.csv')

    def value(self):
        '''Returns the resulting value (only avaibale after calculation)'''
        return self.converter.main_value.value()

    def set_value(self, val):
        self.converter.main_value.update(val)

    def etm_key(self):
        '''Returns the etm key of the main value'''
        return self.converter.main_value.key

    def endpoint(self):
        return self.converter.main_value.endpoint
