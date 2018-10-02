from flask import Flask, jsonify
app = Flask(__name__)


# Garmin Callbacks
@app.route('/mcog/garmin_cb/dailies', methods=['POST'])
def get_store():
    return jsonify({'message': 'store not found'})


app.run(host='0.0.0.0', port=443, debug=True, ssl_context=(
        "/etc/letsencrypt/live/cmogflaskbackend.minuku.org/cert.pem",
        "/etc/letsencrypt/live/cmogflaskbackend.minuku.org/privkey.pem"))
