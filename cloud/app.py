import crypt
from hmac import compare_digest as compare_hash
import subprocess
from flask import Flask
from flask import request


app = Flask(__name__)

edge_info = {} # TODO: Use a cache or database instead of a built-in dictionary


def username_exists(username):
    result = subprocess.run(['getent', 'passwd', username],
                            capture_output=True)
    output = result.stdout.decode()
    # TODO: Handle exceptions
    return output != ''


def password_matches(username, password):
    result = subprocess.run(f'cat /etc/shadow | grep {username}',
                            shell=True,
                            capture_output=True)
    output = result.stdout.decode()
    # TODO: Handle exceptions
    encrypted_password = output.split(':')[1]
    if not encrypted_password:
        return True
    if encrypted_password == 'x' or encrypted_password == '*':
        raise ValueError('No support for shadow passwords')
    return compare_hash(crypt.crypt(password, encrypted_password),
                        encrypted_password)


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username_exists(username):
        return 'Username already taken'
    subprocess.run(['useradd', '-m', '-g', 'edgetop', username]) # TODO: Try not to hardcode group name
    subprocess.run(f'echo {username}:{password} | chpasswd', shell=True)
    return 'OK'


@app.route('/verify_user', methods=['POST'])
def verify_user():
    username = request.form['username']
    password = request.form['password']
    if not username_exists(username):
        return 'Username does not exist'
    if not password_matches(username, password):
        return 'Password does not match'
    return 'OK'


@app.route('/get_edge_addr', methods=['POST'])
def get_edge_addr():
    if request.form['gateway_addr'] not in edge_info:
        return ''
    return edge_info[request.form['gateway_addr']]


@app.route('/report_edge_info', methods=['POST'])
def report_edge_info():
    edge_info[request.form['gateway_addr']] = request.form['ip_addr']
    return 'OK'
