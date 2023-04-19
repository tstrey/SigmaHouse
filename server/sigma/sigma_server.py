import os
import time
from flask import Flask, render_template, url_for, request, jsonify, session, json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import send_from_directory
from flask_socketio import SocketIO
import subprocess
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.title = "Sigma_Server"
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
client_ips = {
}



@app.route('/xyz/<path:path>')
def send_report(path):
    print('got in xyz')
    client_ip = request.remote_addr
    client_ips[client_ip] = client_ip
    return send_from_directory('mdds', path)

#def handle_update():
#    while True:
#        print('about to send update')
#        socketio.emit('data', '123') # emit an event to the client
#        print('sent update')
#        time.sleep(1) # wait for one second before checking for new data again

@app.route('/mdds')
def mdds():
    print('got in mdds')
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'mdds/standalone/', 'test.json')
    json_resp = json.load(open(json_url))
    print(json_resp)
    #http://192.168.0.101/mdds/standalone/config.json
    print("Setup End")
    return send_from_directory('mdds/standalone/', 'test.json')
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/list_houses', methods=['POST', 'GET'])
def listHouses():
    print('in houses list')
    json_obj = json.dumps(client_ips)
    print(json_obj)
    return jsonify(json_obj)
    
@app.route('/process_house', methods=['POST', 'GET'])
def process_qt_calculation():
  print('in process_qt_calculation')
  if request.method == "POST":
    qtc_data = request.get_json()
    client_ip = request.remote_addr
    client_ips[client_ip] = client_ip
    print(qtc_data)
  results = {'rows': 'Sigma Houses name ' + qtc_data[0]['House_name']}
  return jsonify(results)


if __name__ == "__main__":
    app.run(port=80, threaded=False, use_reloader=True, debug=True, host="0.0.0.0")





