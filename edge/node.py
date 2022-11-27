import requests
from urllib.parse import urljoin
import common
import utility


def report_edge_info():
    url = urljoin(common.cloud_url, '/report_edge_info')
    data = {}
    data['gateway_addr'] = utility.get_gateway_addr()
    data['ip_addr'] = utility.get_ip_addr()
    if requests.post(url, data=data).text != 'OK':
        pass # TODO: Handle exceptions


if __name__ == '__main__':
    report_edge_info()
