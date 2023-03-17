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


def retrieve_results(scenario_id: int, config_dict: dict) -> dict:
    '''
    Retrieves the ETM outputs as specified under the config_dict's 'config' key,
    and returns the results in a dict. Sets the correct CONFIG path for retrieving main
    config like the ETM api url.

    Params:
        scenario_id (int):  ETM scenario ID to communicate with;
        from_dict (dict):   Data requests in dict format; Contains at least the
                            following keys: 'api_url' (url of ETM) and 'config'
                            (a dict of data requests)
    '''
    # Update configs
    Config.FROM_CONF_PATH = False
    Config().api_url = config_dict['api_url']

    # Create requests
    data_requests = DataRequests.from_dict(config_dict['config'])

    return retrieve_from_requests(scenario_id, data_requests)


def retrieve_results_from_ymls(scenario_id, config_path=CONFIG_PATH,
    config_name='etm_service') -> dict:
    '''
    Retrieves the ETM outputs as specified in config ymls, and returns the results in a dict.
    Sets the correct CONFIG path for retrieving main config like the ETM api url.

    Params:
        scenario_id (int):  ETM scenario ID to communicate with;
        config_path (Path): Path to the folder containing the config file(s);
        config_name (str):  This yml file's name will be checked out in the config folder to
                            be loaded into data requests.
    '''
    # Update configs (contains etm api url)
    Config.CONFIG_PATH = config_path / 'config.yml'

    # Create requests
    data_requests = DataRequests.load_from_path(config_path / f'{config_name}.yml')

    return retrieve_from_requests(scenario_id, data_requests)


def retrieve_from_requests(scenario_id: int, data_requests: DataRequests):
    # Send requests
    batches = Batches()

    data_requests.ready(batches)
    batches.send(scenario_id)

    data_requests.convert()

    return data_requests.to_dict()


def scale_copy_and_send(scenario_id: int, holon_outcomes: dict, config_dict: dict) -> int:
    '''
    Scales and updates sliders in the ETM, returns the ETM scenario ID of the copied and
    set scenario.

    Params:
        scenario_id (int):      ETM scenario ID to communicate with;
        holon_outcomes (dict):  Holon outcomes in json or dict format; The keys should match
                                the keys of the data requests
        from_dict (dict):       Data requests in dict format; Contains at least the
                                following keys: 'api_url' (url of ETM) and 'config'
                                (a dict of data requests)

    '''

    # Update configs
    Config.FROM_CONF_PATH = False
    Config().api_url = config_dict['api_url']

    data_requests = DataRequests.from_dict(config_dict['config'], action='SET')

    return scale_copy_and_send_from_requests(scenario_id, holon_outcomes, data_requests)


def scale_copy_and_send_from_ymls(scenario_id, holon_outcomes, config_path=CONFIG_PATH,
    config_name='scaling_factors') -> int:
    '''
    Scales and updates sliders in the ETM, returns the ETM scenario ID of the copied and
    set scenario. Based on Config ymls.

    Params:
        scenario_id (int):      ETM scenario ID to communicate with;
        holon_outcomes (dict):  Holon outcomes in json or dict format
        config_path (Path):     Path to the folder containing the config file(s);
        config_name (str):      This yml file's name will be checked out in the config folder
                                to be loaded into data requests.
    '''
    # Update configs
    Config.CONFIG_PATH = config_path / 'config.yml'

    data_requests = DataRequests.load_from_path(config_path / f'{config_name}.yml', action='SET')

    return scale_copy_and_send_from_requests(scenario_id, holon_outcomes, data_requests)


def scale_copy_and_send_from_requests(scenario_id, holon_outcomes, data_requests: DataRequests):
    '''Called only by the other two scale_copy_and_send methods'''

    # Combine requests with HOLON outcomes
    combiner = Combiner(holon_outcomes)
    data_requests.combine(combiner)

    # Convert first
    data_requests.convert()

    # Balance after conversions
    # I let the engine autobalance for now, should be good enough
    # data_requests.balance()

    # Prepare batches
    batches = Batches(action='SET')
    data_requests.ready(batches)

    # Copy scenario and send
    scenario_copy = next(ETMConnection('copy', scenario_id).connect(None))
    batches.send(scenario_copy)

    return scenario_copy
