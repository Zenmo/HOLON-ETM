import pytest

from etm_service.etm_session.session import ETMConnectionError, ETMSession
from etm_service.etm_session import ETMConnection, InvalidEndpoint
from etm_service.config import Config

@pytest.fixture
def scenario_id():
    return Config().scenario['id']

def test_connection(scenario_id):
    connection = ETMConnection('queries', scenario_id)
    assert isinstance(connection.session, ETMSession)

    with pytest.raises(InvalidEndpoint):
        bad_connection = ETMConnection('kittens', scenario_id)

def test_send_request_to_queries(requests_mock, scenario_id):
    connection = ETMConnection('queries', scenario_id)

    # QUERIES
    requests_mock.put(
        connection.session.url(),
        status_code=200,
        json={
            "gqueries": {
                "costs_of_insulation": {
                    "present": 0.0,
                    "future": 1234567.8,
                    "unit": "euro"
                },
                "costs_of_capital_in_electricity_production": {
                    "present": 1234567.8,
                    "future": 2345678.9,
                    "unit": "euro"
                }
            }
        }
    )

    # Check if this endpoint yields
    result = connection.connect(
        ["costs_of_insulation", "costs_of_capital_in_electricity_production"]
    )

    first_key, first_val = next(result)
    assert first_key == "costs_of_insulation"
    assert first_val == 1234567.8

    second_key, second_val = next(result)
    assert second_key == "costs_of_capital_in_electricity_production"
    assert second_val == 2345678.9

def test_send_request_to_queries_with_non_existent_query(requests_mock, scenario_id):
    connection = ETMConnection('queries', scenario_id)

    requests_mock.put(
        connection.session.url(),
        status_code=422,
        json={
            "errors": ['Unkown gquery: gquery1']
        }
    )

    with pytest.raises(ETMConnectionError):
        result = connection.connect(
            ["costs_of_insulation", "gquery1"]
        )
        next(result)

def test_send_request_to_nodes(requests_mock, nodes_response_data, helpers, scenario_id):
    connection = ETMConnection('nodes', scenario_id)
    nodes = ['industry_chp_combined_cycle_gas_power_fuelmix', 'node_2']

    helpers.mock_nodes_response(requests_mock, nodes_response_data, connection, nodes)

    result = connection.connect(nodes)

    first_key, first_val = next(result)
    assert first_key == nodes[0]
    assert first_val == nodes_response_data

    second_key, second_val = next(result)
    assert second_key == nodes[1]
    assert second_val == nodes_response_data


def test_set_inputs(requests_mock, scenario_id):
    connection = ETMConnection('inputs',scenario_id, action='PUT')
    inputs = {'input_1': 500, 'input_2': 2.5}

    requests_mock.put(
        connection.session.url(),
        status_code=200,
        json={
            "scenario": {} # There is actually more info in here, but we don't use it
        }
    )

    result = connection.connect(inputs)

    assert next(result)

def test_copy_scenario(requests_mock, scenario_id):
    connection = ETMConnection('copy', scenario_id)
    original_id = Config().scenario['id']

    requests_mock.post(
        Config().api_url,
        status_code=200,
        json={
            "id": 12345 # There is actually more info in here, but we don't use it
        }
    )

    result = connection.connect('')

    assert next(result) != original_id
