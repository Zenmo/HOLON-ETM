#  Module init
from pathlib import Path
from pydoc import resolve

from etm_service.batches import Batches
from etm_service.data_requests import DataRequests
from etm_service.config import Config

CONFIG_PATH = Path(__file__).parents[2].resolve() / 'config' /'etm_service.yml'

def retrieve_results_and_write():
    data_requests = DataRequests.load_from_path(CONFIG_PATH)
    batches = Batches()

    data_requests.ready(batches)
    batches.send()

    data_requests.convert()

    destination = Path(Config().output_folder).resolve()
    destination.mkdir(exist_ok=True)
    data_requests.write_to(destination)
