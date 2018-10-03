from flask import Flask, jsonify, request
app = Flask(__name__)

# use public url: cmogflaskbackend.minuku.org
# Garmin Callbacks


@app.route('/mcog/garmin_cb/<string:name>', methods=['POST'])
def garmin_cb(name):
    request_data = request.get_json()
    print(request_data)
    return jsonify({'message': 'store not found'})


app.run(host='0.0.0.0', port=443, debug=True, ssl_context=(
        "/etc/letsencrypt/live/cmogflaskbackend.minuku.org/fullchain.pem",
        "/etc/letsencrypt/live/cmogflaskbackend.minuku.org/privkey.pem"))
