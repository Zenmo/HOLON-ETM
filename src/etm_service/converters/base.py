class BaseConverter:
    def __init__(self, *values):
        self.children = []

    def calculate(self):
        pass

    def required_for_calculation(self):
        yield

    def add_child(self, child):
        self.children.append(child)
