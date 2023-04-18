import pytest
import numpy as np
from pathlib import Path
import json

from etm_service.single_request import SingleRequest, MissingRequestInfoException
from etm_service.curve import Curve
from etm_service.value import Value
from etm_service.converters import DivideBy
from etm_service.node_property import NodeProperty


@pytest.fixture
def request_with_curve():
    return SingleRequest(
        "buildings_heating_electricity_curve",
        "GET",
        value={"data": "curve", "etm_key": "the_curve_key", "type": "query"},
        convert_with=[
            {
                "data": "curve",
                "etm_key": "the_query_key",
                "conversion": "divide",
                "type": "query",
            }
        ],
    )


@pytest.fixture
def request_with_curve_and_node_property():
    return SingleRequest(
        "buildings_heating_electricity_curve",
        "GET",
        value={"data": "curve", "etm_key": "the_curve_key", "type": "query"},
        convert_with=[
            {
                "data": "technical.electricity_output_conversion.future",
                "etm_key": "industry_chp_combined_cycle_gas_power_fuelmix",
                "type": "node_property",
                "conversion": "divide",
            }
        ],
    )


def test_request_with_curve_divide(request_with_curve):
    # Check if the key is set
    assert request_with_curve.key == "buildings_heating_electricity_curve"

    # Check the values
    values = request_with_curve.values()
    main_value = next(values)
    assert isinstance(main_value, Curve)
    assert main_value.is_set() == False
    assert main_value.key == "the_curve_key"

    second_value = next(values)
    assert isinstance(second_value, Value)
    assert second_value.is_set() == False
    assert second_value.key == "the_query_key"

    # Check the converter
    assert request_with_curve.converter
    assert isinstance(request_with_curve.converter, DivideBy)


def test_calculate(request_with_curve):
    # Set some values
    request_with_curve.converter.main_value.update(np.ones(8760))
    request_with_curve.converter.second_value.update(2)

    request_with_curve.calculate()

    # Did the converter run?
    assert request_with_curve.converter.main_value.sum() == 8760 / 2


def test_request_with_curve_and_node_property(request_with_curve_and_node_property):
    # Check if the key is set
    assert (
        request_with_curve_and_node_property.key
        == "buildings_heating_electricity_curve"
    )

    # Check the values
    values = request_with_curve_and_node_property.values()
    main_value = next(values)
    assert isinstance(main_value, Curve)
    assert main_value.is_set() == False
    assert main_value.key == "the_curve_key"

    second_value = next(values)
    assert isinstance(second_value, NodeProperty)
    assert second_value.is_set() == False
    assert second_value.key == "industry_chp_combined_cycle_gas_power_fuelmix"

    # Check the converter
    assert request_with_curve_and_node_property.converter
    assert isinstance(request_with_curve_and_node_property.converter, DivideBy)


def test_request_without_correct_value_properties():
    # With just one value with typos - this is OK here, it will probably mess up
    # somewhere in the batches
    SingleRequest(
        "some_key",
        "GET",
        value={"data": "curves", "etm_key": "the_curve_key", "type": "query"},
    )

    # With one value with 'type' missing
    with pytest.raises(MissingRequestInfoException):
        SingleRequest(
            "some_key", "GET", value={"data": "curve", "etm_key": "the_curve_key"}
        )

    # With an unknown conversion
    with pytest.raises(MissingRequestInfoException):
        SingleRequest(
            "buildings_heating_electricity_curve",
            "GET",
            value={"data": "curve", "etm_key": "the_curve_key", "type": "query"},
            convert_with=[
                {
                    "data": "curve",
                    "etm_key": "the_query_key",
                    "conversion": "kittens",
                    "type": "query",
                }
            ],
        )

    # With a conversion that takes a second value, where this value is not specified
    with pytest.raises(MissingRequestInfoException):
        SingleRequest(
            "buildings_heating_electricity_curve",
            "GET",
            value={"data": "curve", "etm_key": "the_curve_key", "type": "query"},
            convert_with=[{"conversion": "divide"}],
        )


def test_values():
    request = SingleRequest(
        "buildings_heating_electricity",
        "SET",
        value={"data": "value", "etm_key": "the_etm_key", "type": "inputs"},
        convert_with=[
            {
                "key": "scaling_factor_x",
                "conversion": "multiply",
                "value": 500,
                "type": "static",
            }
        ],
    )

    request.set_value(10)

    request_values = request.values()
    # Only send the first value as required for calculation
    assert next(request_values).value() == 10
    with pytest.raises(StopIteration):
        next(request_values)

    request.calculate()

    assert request.value() == 10 * 500


def test_with_multiple_conversions():
    request = SingleRequest(
        "buildings_heating_electricity",
        "SET",
        value={"data": "value", "etm_key": "the_etm_key", "type": "inputs"},
        convert_with=[
            {
                "key": "scaling_factor_x",
                "conversion": "multiply",
                "value": 500,
                "type": "static",
            },
            {
                "key": "scaling_factor_y",
                "conversion": "multiply",
                "value": 10,
                "type": "static",
            },
            {
                "key": "scaling_factor_y",
                "conversion": "divide",
                "value": 5,
                "type": "static",
            },
        ],
    )

    request.set_value(10)

    request_values = request.values()
    # Only send the first value as required for calculation
    assert next(request_values).value() == 10
    with pytest.raises(StopIteration):
        next(request_values)

    request.calculate()

    assert request.value() == 10 * 500 * 10 / 5

def test_inproduct():

    c1 = Curve("curve_key", endpoint="GET", value=np.array([1,2,3]))

    c2 = Curve("curve_key", endpoint="GET", value=np.array([4,5,6]))
    c1.multiply(c2)


    assert c1.value() == 32

def test_inproduct_request():
    anylogic_curve = json.loads(
        (Path(__file__).parent / "fixtures" / "anylogic_result_curve.json").read_text()
    )
    request = SingleRequest(
        "buildings_heating_electricity",
        "GET",
        value={"data": "curve", "etm_key": "the_etm_key", "type": "query"},
        convert_with=[
            {
                "key": "scaling_factor_x",
                "conversion": "in_product",
                "value": anylogic_curve,
                "type": "static",
                "data": "curve",
            },
        ],
    )

    request.converter.main_value.update(np.ones(8760))
    request.calculate()

    assert round(request.value(),2) == round(request.converter.second_value.value().sum(),2)

