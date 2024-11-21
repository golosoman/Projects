from prefect import flow
from utils import upload

@flow(log_prints=True)
def parse():
  upload({ 'name': 'Stub', 'systemName': 'Stub', 'residentialComplexes': [] })
