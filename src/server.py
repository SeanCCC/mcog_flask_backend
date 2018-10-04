from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from constants import Constants

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
mongo = PyMongo(app)

@app.route('/mcog/garmin_api/dailies', methods=['POST'])
def insert_dailies():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.dailies.insert(request_data)
    return '', 200

@app.route('/mcog/garmin_api/activities', methods=['POST'])
def insert_activities():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.activities.insert(request_data)
    return '', 200

@app.route('/mcog/garmin_api/manually_updated_activities', methods=['POST'])
def insert_manually_updated_activities():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.manually_updated_activities.insert(request_data)
    return '', 200

@app.route('/mcog/garmin_api/epochs', methods=['POST'])
def insert_epochs():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.epochs.insert(request_data)
    return '', 200

@app.route('/mcog/garmin_api/sleeps', methods=['POST'])
def insert_sleeps():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.sleeps.insert(request_data)
    return '', 200

@app.route('/mcog/garmin_api/body_compositions', methods=['POST'])
def insert_body_compositions():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.body_compositions.insert(request_data)
    return '', 200

@app.route('/mcog/garmin_api/third_party_dailies', methods=['POST'])
def insert_third_party_dailies():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.third_party_dailies.insert(request_data)
    return '', 200

@app.route('/mcog/garmin_api/stress', methods=['POST'])
def insert_stress():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.stress.insert(request_data)
    return '', 200

@app.route('/mcog/garmin_api/user_metrics', methods=['POST'])
def insert_user_metrics():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.user_metrics.insert(request_data)
    return '', 200

@app.route('/mcog/garmin_api/moveIQ', methods=['POST'])
def insert_moveIQ():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.moveIQ.insert(request_data)
    return '', 200

@app.route('/mcog/garmin_api/pulse_ox', methods=['POST'])
def insert_pulse_ox():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    mongo.db.pulse_ox.insert(request_data)
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=(
	Constants.FULLCHAIN,
        Constants.PRIVKEY))
