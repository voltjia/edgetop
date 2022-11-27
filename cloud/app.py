from flask import Flask
from flask import request


app = Flask(__name__)

edge_info = {} # TODO: Use a cache or database instead of a built-in dictionary
user_info = {} # TODO: Use a cache or database instead of a built-in dictionary


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username in user_info:
        return 'Username already taken'
    user_info[username] = password
    return 'OK'


@app.route('/verify_user', methods=['POST'])
def verify_user():
    username = request.form['username']
    password = request.form['password']
    if username not in user_info:
        return 'Invalid username'
    if password != user_info[username]:
        return 'Invalid password'
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
