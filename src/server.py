from flask import Flask, jsonify, request, Response
from constants import Constants

app = Flask(__name__)


@app.route('/', methods=['POST'])
def test_post():
    print(request.get_json(force=True, silent=True))
    return jsonify({'message': 'Recieved'})

@app.route('/mcog/garmin_api/dailies', methods=['POST'])
def dailies():
    request_data = request.get_json(force=True, silent=True)
    print(request_data)
    return '', 200
#    return Response(Constants.API_RESPONSE, status=200, mimetype='application/json')
#    return jsonify({'message': 'store not found'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, debug=True, ssl_context=(
	Constants.FULLCHAIN,
        Constants.PRIVKEY))
