from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))) + '/src')

import etm_service

if __name__ == '__main__':
    scenario_id = 1647734
    config_name = 'poc'

    results = etm_service.retrieve_results(scenario_id, config_name)

    print(results)

