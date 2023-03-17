from .base import BaseConverter

class WithTwoValuesConverter(BaseConverter):
    def __init__(self, main_value, second_value):
        super().__init__()
        self.main_value = main_value
        self.second_value = second_value

    def required_for_calculation(self):
        '''Generator, returns all Values that should be requested from the ETM'''
        if not self.main_value.static:
            yield self.main_value
        if not self.second_value.static:
            yield self.second_value

    def calculate_children(self):
        for converter in self.children:
            converter.main_value = self.main_value
            converter.calculate()
            self.main_value = converter.main_value
