"""Main Flask app."""
from connexion import App

from flask import render_template, jsonify, request

from datetime import datetime

from iot_hub_mockup.houses import HOUSES

app = App(__name__, specification_dir="./")
app.add_api("swagger.yml")


@app.route("/")
def home():
    """Serve landing page."""
    return render_template("index.html")

@app.route("/updateIps")
def updateIps():
    """Serve landing page."""
    print("In updateIps")
    return render_template("index.html")

@app.route("/smarthouse/v1/houses", methods=["GET"])
def get_houses():
    return jsonify(HOUSES), 200

@app.route("/smarthouse/v1/houses", methods=["POST"])
def create_house():
    print("in /smarthouse/v1/houses")
    client_ip = request.remote_addr
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    house_data = request.json
    print(house_data)
    house_data['ip_address'] = client_ip
    house_data['timestamp'] = timestamp
    HOUSES.append(house_data)
    print(house_data)
    return house_data, 201

# Update an item
@app.route("/smarthouse/v1/houses/{id}", methods=["PUT"])
def update_house(id, item_data):
    print("in /smarthouse/v1/houses/{id}")
    client_ip = request.remote_addr
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    house_data = request.json
    print(house_data)
    house_data['ip_address'] = client_ip
    house_data['timestamp'] = timestamp
    return house_data, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)  # noqa: S201, S104
