from flask import Flask, jsonify
app = Flask(__name__)

# use public url: cmogflaskbackend.minuku.org

# Garmin Callbacks
@app.route('/mcog/garmin_cb/dailies', methods=['POST'])
def dailies_cb():
    return jsonify({'message': 'store not found'})


@app.route('/mcog/garmin_cb/activities', methods=['POST'])
def activitis_cb():
    return jsonify({'message': 'store not found'})


@app.route('/mcog/garmin_cb/manuallyupatedact', methods=['POST'])
def manuallyupatedact_cb():
    return jsonify({'message': 'store not found'})


@app.route('/mcog/garmin_cb/epochs', methods=['POST'])
def epochs_cb():
    return jsonify({'message': 'store not found'})


@app.route('/mcog/garmin_cb/sleeps', methods=['POST'])
def sleeps_cb():
    return jsonify({'message': 'store not found'})


@app.route('/mcog/garmin_cb/bodycomperessions', methods=['POST'])
def bodycomperessions_cb():
    return jsonify({'message': 'store not found'})


@app.route('/mcog/garmin_cb/thirdpartydailies', methods=['POST'])
def thirdpartydailies_cb():
    return jsonify({'message': 'store not found'})


@app.route('/mcog/garmin_cb/stress', methods=['POST'])
def stress_cb():
    return jsonify({'message': 'store not found'})


@app.route('/mcog/garmin_cb/usermetrics', methods=['POST'])
def usermetrics_cb():
    return jsonify({'message': 'store not found'})


@app.route('/mcog/garmin_cb/movelq', methods=['POST'])
def movelq_cb():
    return jsonify({'message': 'store not found'})


@app.route('/mcog/garmin_cb/pulseox', methods=['POST'])
def pulseox_cb():
    return jsonify({'message': 'store not found'})


app.run(host='0.0.0.0', port=443, debug=True, ssl_context=(
        "/etc/letsencrypt/live/cmogflaskbackend.minuku.org/fullchain.pem",
        "/etc/letsencrypt/live/cmogflaskbackend.minuku.org/privkey.pem"))
