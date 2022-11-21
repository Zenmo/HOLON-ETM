from etm_service.data_requests import DataRequests
from etm_service.single_request import SingleRequest
from etm_service.batches import Batches
from etm_service.combiner import Combiner

def test_load(config_path):
    data_requests = DataRequests.load_from_path(config_path)

    # Check if it has loaded at least one
    assert next(data_requests.all())

    # Is it a request?
    assert isinstance(next(data_requests.all()), SingleRequest)

def test_ready_batches(config_path):
    data_requests = DataRequests.load_from_path(config_path)
    batches = Batches()

    # Quick check up front
    for batch in batches.each():
        assert batch.is_empty()

    # Ready them
    data_requests.ready(batches)

    # Is there something in them now?
    for batch in batches.each():
        if batch.endpoint == 'nodes' or batch.endpoint == 'curves' or batch.endpoint == 'inputs':
            continue # Not yet implemented in the test

        assert not batch.is_empty()

def test_load_with_set_action(config_path_scaling):
    data_requests = DataRequests.load_from_path(config_path_scaling, action='SET')

    single_req = next(data_requests.all())

    assert single_req.action == 'SET'


def test_balance_transport_truck_using_electricity_share(config_path_scaling):
    data_requests = DataRequests.load_from_path(config_path_scaling, action='SET')

    request_amount = len(data_requests.data_requests)

    data_requests.combine(Combiner({
        'name_of_holon_input_eletric_trucks': 101,
    }))


    #  TODO: Ze gaan er niet juist in en blijven 0 FUCK
    data_requests.balance()

    # Adds one request
    assert len(data_requests.data_requests) == request_amount + 1

    # This request has value 0, and the original one 100
    for request in data_requests.all():
        if request.etm_key() == 'transport_truck_using_diesel_mix_share':
            assert request.value() == 0
        elif request.etm_key() == 'transport_truck_using_electricity_share':
            assert request.value() == 100
