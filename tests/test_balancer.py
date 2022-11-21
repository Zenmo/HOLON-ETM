import pytest

from etm_service.balancer import Balancer, BALANCING_GROUPS
from etm_service.single_request import SingleRequest

@pytest.fixture
def basic_request():
    return SingleRequest(
        'balance_me',
        'SET',
        value={
            'data': 'value',
            'type': 'input',
            'etm_key': BALANCING_GROUPS[0][0]
        }
    )


def test_balancer_with_setting_inputs_over_100(basic_request):
    balancer = Balancer()

    # Should result in extra request with 0 and this one lowered to 100
    basic_request.set_value(101.0)

    balancer.add(basic_request)

    extra_requests = balancer.resolve()

    assert extra_requests
    assert extra_requests[0].key.startswith(BALANCING_GROUPS[0][1])
    assert extra_requests[0].value() == 0

    assert basic_request.value() == 100


def test_balancer_with_setting_inputs_under_100(basic_request):
    balancer = Balancer()

    # Should result in extra request with 5 and this one upped to 95
    basic_request.set_value(90.0)

    balancer.add(basic_request)

    extra_requests = balancer.resolve()

    assert extra_requests
    assert extra_requests[0].key.startswith(BALANCING_GROUPS[0][1])
    assert extra_requests[0].value() == 5

    assert basic_request.value() == 95


def test_balancer_with_setting_inputs_to_zero(basic_request):
    balancer = Balancer()

    # Should result in nothing happening
    basic_request.set_value(0)

    balancer.add(basic_request)

    extra_requests = balancer.resolve()

    assert not extra_requests
    assert not basic_request.converter.main_value.is_set()
