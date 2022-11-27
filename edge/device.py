import requests
from urllib.parse import urljoin
import common
import utility


def get_edge_addr():
    url = urljoin(common.cloud_url, '/get_edge_addr')
    data = {'gateway_addr': utility.get_gateway_addr()}
    response = requests.post(url, data=data)
    if response.text == '':
        pass # TODO: Handle exceptions
    return response.text


if __name__ == '__main__':
    edge_addr = get_edge_addr()
