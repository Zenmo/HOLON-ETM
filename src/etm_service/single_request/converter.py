from etm_service.curve import Curve
from etm_service.value import Value
from etm_service.node_property import NodeProperty
import etm_service.converters as converters

class RequestConverter:
    @property
    def converter(self):
        return self._converter

    @converter.setter
    def converter(self, config):
        self._converter = self._create_converter(
            self._as_value(config.pop('value')),
            config
        )

    # Private

    def _as_value(self, value_data):
        '''Unpacks data and returns a Value based on it'''
        return self._value_for(*self._safe_value_params(value_data))

    def _value_for(self, key, data, endpoint):
        '''
        Extract which type of data we're dealing with, can be a Curve or a single value
        '''
        if endpoint == "static":
            return Value(key, value=data, static=True)
        elif data == "curve":
            return Curve(key, endpoint)
        elif endpoint == "node_property":
            return NodeProperty(key, node_property=data, endpoint=endpoint)
        else:
            return Value(key, endpoint)

    def _safe_value_params(self, value_data):
        '''Return some reasonable info to the user if they messed up the config'''
        try:
            if value_data['type'] == 'static':
                return value_data['key'], value_data['value'], value_data['type']

            return value_data['etm_key'], value_data['data'], value_data['type']
        except KeyError as err:
            raise MissingRequestInfoException(f'Missing field {str(err)} in {self.key}') from err

    def _create_converter(self, main_value, converter_config):
        '''
        Set the converter and any additional value needed (e.g. DivideBy)

        Assumes the divide_by is not another curve, just a query!

        Params:
            main_value(Value):          The Value that should be converted
            converter_config(kwargs):   Has at least the key 'conversion'. Used to determine the
                                        converter for this data request.
        '''
        conversion = converter_config.pop('conversion', None)
        if conversion == 'divide' and 'convert_with_value' in converter_config:
            return converters.DivideBy(
                main_value,
                self._as_value(converter_config.pop('convert_with_value'))
            )
        if conversion == 'multiply' and 'convert_with_value' in converter_config:
            return converters.Multiply(
                main_value,
                self._as_value(converter_config.pop('convert_with_value'))
            )
        if not conversion:
            return converters.Empty(main_value)

        raise MissingRequestInfoException(
            f"Can not create conversion '{conversion}' for {self.key}")


class MissingRequestInfoException(BaseException):
    pass
