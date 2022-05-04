from flask import Flask, request, json, make_response

app = Flask(__name__)


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

    return make_response(data)


if __name__ == '__main__':
    app.run()
