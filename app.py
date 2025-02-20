from flask import Flask


app = Flask(__name__)


@app.route('/')
def main_page():
    return '<h1>Миссия Колонизация Марса</h1>'


@app.route('/index')
def index():
    return '<h1>И на Марсе будут яблони цвести!</h1>'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
