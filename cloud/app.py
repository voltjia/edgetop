from flask import Flask
from flask import request


app = Flask(__name__)

edge_info = {} # TODO: Use a cache or database instead of a built-in dictionary


@app.route('/get_edge_addr', methods=['POST'])
def get_edge_addr():
    if request.form['gateway_addr'] not in edge_info:
        return ''
    return edge_info[request.form['gateway_addr']]


@app.route('/report_edge_info', methods=['POST'])
def report_edge_info():
    if 'gateway_addr' not in request.form or 'ip_addr' not in request.form:
        return ''
    edge_info[request.form['gateway_addr']] = request.form['ip_addr']
    return 'OK'
