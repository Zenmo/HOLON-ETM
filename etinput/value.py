import numpy as np

class Value:
    def __init__(self, key, endpoint='query', value=None):
        '''
        Respresents a value. Values contain info about their ETM key and endpoint,
        and extra information if needed. A (numeric) value is not set at initialisation
        and can be updated after connecting to the ETM.
        '''
        self.key = key
        self.endpoint = endpoint
        self._value = value

    def is_set(self):
        '''Bool, returns if the value is set'''
        if self._value is None:
            return False

        return True

    def update(self, value):
        '''Updates the value'''
        self._value = float(value)

    ## Conversions

    def multiply(self, other):
        '''Multiplies itself with the other Value'''
        self._value = self._value * other._value

    def divide_by(self, other):
        '''Divides itself by the other Value, validates this Value is not zero'''
        if other._value == 0:
            return

        self._value = self._value / other._value

    ##

    def _value_as_np(self):
        return np.array([self._value])

    def write_to(self, path):
        '''Writes the values as a CSV to the given path'''
        if self.is_set():
            np.savetxt(path, self._value_as_np(), delimiter=',')
        else:
            raise ValueError(f'{str(self)} was not yet set or updated.')

    def __str__(self):
        return f'{self.__class__.__name__}({self.key})'