from collections import deque
import json
import socket
import subprocess
import requests
from urllib.parse import urljoin
import common
import utility


MAX_NUM_USERS = 32

user_assignment = {} # TODO: Use a cache or database instead of a built-in dictionary
unused_display_nums = deque()
for i in range(2, MAX_NUM_USERS + 2):
    unused_display_nums.append(i)


def report_edge_info():
    url = urljoin(common.CLOUD_URL, '/report_edge_info')
    data = {}
    data['gateway_addr'] = utility.get_gateway_addr()
    data['ip_addr'] = utility.get_ip_addr()
    if requests.post(url, data=data).text != 'OK':
        pass # TODO: Handle exceptions


def is_valid_login(username, password):
    url = urljoin(common.CLOUD_URL, '/verify_user')
    data = {'username': username, 'password': password}
    response = requests.post(url, data=data)
    if response.text != 'OK':
        return False
    return True


def assign_user(username):
    if username in user_assignment:
        return
    user_assignment[username] = unused_display_nums.popleft()


def generate_user_assignment_file():
    user_assignment_str = ''
    for username, display_num in user_assignment.items():
        user_assignment_str += f':{display_num}={username}\n'
    with open('/etc/tigervnc/vncserver.users', 'w', encoding="utf-8") as f:
        f.write(user_assignment_str)


def start_display(display_num):
    subprocess.run(['systemctl', 'start', f'vncserver@:{display_num}.service'])


if __name__ == '__main__':
    report_edge_info()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', common.EDGE_PORT))
        sock.listen()
        while True:
            conn, _ = sock.accept()
            with conn:
                data = json.loads(conn.recv(common.BUFSIZE).decode('utf-8'))
                if 'username' not in data:
                    conn.sendall(b'No username provided')
                    break
                if 'password' not in data:
                    conn.sendall(b'No password provided')
                    break
                username = data['username']
                password = data['password']
                if not is_valid_login(username, password):
                    conn.sendall(b'Invalid username or password')
                    break
                assign_user(username)
                display_num = user_assignment[username]
                generate_user_assignment_file()
                start_display(display_num)
                port = common.EDGE_PORT + display_num
                conn.sendall(str(port).encode('utf-8'))

    # TODO: Report again when shutting down
