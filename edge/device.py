import json
import getpass
import socket
import subprocess
import requests
from urllib.parse import urljoin
import common
import utility


def get_edge_addr():
    url = urljoin(common.CLOUD_URL, '/get_edge_addr')
    data = {'gateway_addr': utility.get_gateway_addr()}
    response = requests.post(url, data=data)
    if response.text == '':
        pass # TODO: Handle exceptions
    return response.text


def login():
    edge_addr = get_edge_addr()
    username = input('Username: ')
    password = getpass.getpass()
    pin = getpass.getpass('PIN: ')
    data = {'username': username, 'password': password, 'pin': pin}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((edge_addr, common.EDGE_PORT))
        sock.sendall(json.dumps(data).encode('utf-8'))
        data = sock.recv(common.BUFSIZE).decode('utf-8')
        if data == '':
            return # TODO: Handle exceptions
    port = data
    subprocess.run(['vncviewer', 'FullScreen=1', f'{edge_addr}::{port}'])


if __name__ == '__main__':
    login()
