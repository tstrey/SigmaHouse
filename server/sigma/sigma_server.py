import os
import time
from flask import Flask, render_template, url_for, request, jsonify, session, json
from flask import send_from_directory
from flask_socketio import SocketIO
from datetime import datetime
import subprocess
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.title = "Sigma_Server"
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
client_ips = {
}
house_ips = {
}   

@app.route('/')
def index():
  print("in index")
  return render_template('index.html')

@app.route('/houses')
def houses_test():
  print("in houses")
  return render_template('houses.html')

@app.route('/register')
def register():
  print("in register")
  result = {'already': ''}
  client_ip = request.remote_addr
  # Get current timestamp
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  if client_ip not in client_ips:
      client_ips[client_ip] = timestamp
      result = {'ip': client_ip, 'timestamp': timestamp}  
  else:
    client_ips[client_ip] = timestamp
    result = {'already': client_ip}  
  print(result)  
  return jsonify(result)

@app.route('/registerHouse')
def registerHouse():
  print("in register house")
  result = {'already': ''}
  house_ip = request.remote_addr
  # Get current timestamp
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  if house_ip not in house_ips:
      house_ips[house_ip] = timestamp
      result = {'ip': house_ip, 'timestamp': timestamp}  
  else:
    house_ips[house_ip] = timestamp
    result = {'already': house_ip}  
  print(result)  
  return jsonify(house_ips)

@app.route('/updateIps')
def updateIps():
  print("in updateIps")
  json_list = []
  for key in client_ips:
    clientIp = {'ip': key, 'timestamp': client_ips[key]}
    json_list.append(clientIp) 
  return jsonify(json_list)

@app.route('/updateHouses')
def updateHouses():
  print("in updateHouses")
  json_list = []
  for key in house_ips:
    houseIp = {'ip': key, 'timestamp': house_ips[key]}
    json_list.append(houseIp) 
  return jsonify(json_list)


@app.route('/clearIps')
def clearIps():
  print("in clear")
  client_ips.clear()
  return jsonify({'empty': ''})


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
    print(SITE_ROOT)
    json_url = os.path.join(SITE_ROOT, 'mdds/standalone/', 'test.json')
    json_resp = json.load(open(json_url))
    print(json_resp)
    #http://192.168.0.101/mdds/standalone/config.json
    print("Setup End")
    return send_from_directory('mdds/standalone/', 'test.json')



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
    print('about to start server')
    app.run(port=80, threaded=False, use_reloader=True, debug=True, host="0.0.0.0")





