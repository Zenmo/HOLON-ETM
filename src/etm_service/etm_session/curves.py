import requests

from .session import ETMSession

class ETMSetCurvesSession(ETMSession):
    ENDPOINT = '/custom_curves'

    def send_request(self, curves):
        for curve_key, curve_value in curves.items():
            self._handle_response(
                requests.put(f'{self.url()}/{curve_key}',
                files=self._curve_as_file(curve_key, curve_value))
            )
            yield True

    def _handle_response(self, response):
        if response.ok:
            return

        return super()._handle_response(response)

    def _curve_as_file(self, curve_key, curve):
        curve_string = '\n'.join(str(e) for e in curve)
        return {'file': (f'HOLON_{curve_key}', curve_string)}
