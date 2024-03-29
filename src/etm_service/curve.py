import numpy as np

from etm_service.value import Value


class Curve(Value):
    def __init__(self, key, endpoint="query", value=np.array(0), **kwargs):
        """Values should be an np.array of 8760 - add validations"""
        super().__init__(key, endpoint=endpoint, value=value, **kwargs)

    def is_set(self):
        """Bool, returns if the value is set"""
        if self._value.size == 1 and isinstance(self._value, np.ndarray):
            return False

        return True

    def update(self, array):
        """Updates the value"""
        self._value = np.array(array)

    def sum(self):
        """Only used for validation"""
        return self._value.sum()

    def multiply(self, other):
        if isinstance(other, Curve):
            self._value = np.inner(self._value, other._value)
        else:
            super().multiply(other)

    # Later we can add other actions like summing curves, multiplying, etc. We can move
    # them to a module 'operations' when there are starting to be too many

    def _value_as_np(self):
        return self._value
