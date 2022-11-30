#  Module init
from pathlib import Path

from etm_service.batches import Batches
from etm_service.data_requests import DataRequests
from etm_service.etm_session import ETMConnection
from etm_service.combiner import Combiner
from etm_service.config import Config

CONFIG_PATH = Path(__file__).parents[2].resolve() / 'config'

def retrieve_results_and_write():
    # Basic scenario
    scenario_id = 1647734

    data_requests = DataRequests.load_from_path(CONFIG_PATH)
    batches = Batches(scenario_id)

    data_requests.ready(batches)
    batches.send()

    data_requests.convert()

    destination = Path(Config().output_folder).resolve()
    destination.mkdir(exist_ok=True)
    data_requests.write_to(destination)


def retrieve_results(scenario_id, config_path=CONFIG_PATH, config_name='etm_service') -> dict:
    '''
    Retrieves the ETM outputs as specified in the config, and returns the results in a dict
    '''
    # Update configs
    Config.CONFIG_PATH = config_path / 'config.yml'

    # Create and send requests
    data_requests = DataRequests.load_from_path(config_path / f'{config_name}.yml')

    batches = Batches()

    data_requests.ready(batches)
    batches.send(scenario_id)

    data_requests.convert()

    return data_requests.to_dict()


def scale_copy_and_send(scenario_id, holon_outcomes, config_path=CONFIG_PATH, config_name='scaling_factors') -> int:
    '''
    Scales and updates sliders in the ETM, returns the ETM scenario ID of the copied and
    set scenario.
    '''

    # Update configs
    Config.CONFIG_PATH = config_path / 'config.yml'

    # Create requests
    data_requests = DataRequests.load_from_path(config_path / f'{config_name}.yml', action='SET')

    # Combine requests with HOLON outcomes
    combiner = Combiner(holon_outcomes)
    data_requests.combine(combiner)

    # Convert first
    data_requests.convert()

    # Balance after conversions
    data_requests.balance()

    # Prepare batches
    batches = Batches(action='SET')
    data_requests.ready(batches)

    # Copy scenario and send
    scenario_copy = next(ETMConnection('copy', scenario_id).connect(None))
    batches.send(scenario_copy)

    return scenario_copy
