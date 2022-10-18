'''
Please install the pipenv environnement first:
`pipenv install --ignore-pipfile`

Then you can run the module by running this script :)
Or incorporate it somwehere else!
'''
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))) + '/src')

import etm_service

if __name__ == '__main__':
    etm_service.retrieve_results_and_write()

