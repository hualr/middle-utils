from flask import Flask, request, json, make_response, jsonify
import logging

from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# logger = logging.getLogger('atp_log')
# logger.setLevel(logging.DEBUG)


@app.route('/')
def index():
    return 'hello world'


@app.route('/hi1')
def hi():
    param = request.args['hello']

    if param is None:
        param = "unkown"
    return '<h1>' + param + '</h1>'


@app.route('/hi2')
def hi2():
    data = {
        "name": 1
    }

    return make_response(data)\

@app.route('/hi3')
def hi3():
    print(1/0)
    data = {
        "name": 1
    }

    return make_response(data)


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # 这样获取就可以了
        json_data = request.json
        logging.info(f"json_data:{json_data}")
        return jsonify(json_data)


if __name__ == '__main__':
    app.run()
