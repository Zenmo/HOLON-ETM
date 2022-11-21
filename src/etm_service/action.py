class Action():
    '''Action property'''

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        if value in ['GET', 'SET']:
            self._action = value
        else:
            raise ValueError('Actions can only be "GET" or "SET"')
