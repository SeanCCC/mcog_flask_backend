from flask import Flask, jsonify
app = Flask(__name__)


# Garmin Callbacks
@app.route('/mcog/garmin_cb/dailies', methods=['POST'])
def get_store():
    return jsonify({'message': 'store not found'})


app.run(host='0.0.0.0', port=5000, debug=True)
