import pytest

from etm_service.combiner import Combiner, RequestsToOne
from etm_service.data_requests import DataRequests
from etm_service.single_request import SingleRequest, MissingRequestInfoException

@pytest.fixture
def holon_outcomes():
    return {
        'energy_power_solar_pv_solar_radiation_capacity': 10,
        'other_outcome': 5.5
    }

def test_combiner(holon_outcomes, config_path_scaling):
    data_requests = DataRequests.load_from_path(config_path_scaling, action='SET')

    # This should be the one with 'energy_power_solar_pv_solar_radiation_capacity'
    single_req = next(data_requests.all())

    combiner = Combiner(holon_outcomes)

    # assert value was not set indeeed
    with pytest.raises(ValueError):
        single_req.value()

    combiner.inject(single_req)

    assert single_req.value() == 10

    # Now test with a single request that has no holon data

    other_single_req = SingleRequest(
        'some_key', 'SET', **{
            'value': {
                'type': 'inputs',
                'data': 'value',
                'etm_key': 'capacity_of_energy_power_solar_pv_solar_radiation'
                }
            }
    )

    # assert value was not set indeeed
    with pytest.raises(ValueError):
        other_single_req.value()

    combiner.inject(other_single_req)

    # Nothing happened
    with pytest.raises(ValueError):
        other_single_req.value()


def test_combiner(holon_outcomes, config_path_scaling):
    data_requests = DataRequests.load_from_path(config_path_scaling, action='SET').all()

    # This should be the one with 'energy_power_solar_pv_solar_radiation_capacity'
    single_req = next(data_requests)

    combiner = RequestsToOne()

    # assert value was not set indeeed
    with pytest.raises(ValueError):
        single_req.value()

    combiner.inject(single_req)
    assert single_req.value() == 1.0

    single_req_2 = next(data_requests)
    # This one has no conversions so it should fail
    with pytest.raises(MissingRequestInfoException):
        combiner.inject(single_req_2)
