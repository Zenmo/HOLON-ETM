from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))) + '/src')

from pathlib import Path
import etm_service

if __name__ == '__main__':
    scenario_id = 2162987
    config_path = Path(__file__).parents[1].resolve() / 'config'
    config_name = 'scaling_factors'
    holon_outcomes = {
        'energy_power_solar_pv_solar_radiation_capacity': 10
    }

    new_scenario_id = etm_service.scale_copy_and_send(scenario_id, holon_outcomes, config_path, config_name)

    print(new_scenario_id)
