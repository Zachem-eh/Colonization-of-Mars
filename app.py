from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main_page():
    return '<h1>Миссия Колонизация Марса</h1>'


@app.route('/index')
def index():
    return '<h1>И на Марсе будут яблони цвести!</h1>'


@app.route('/promotion')
def promotion():
    return '''Человечество вырастает из детства.<br><br>
    Человечеству мала одна планета.<br><br>
    Мы сделаем обитаемыми безжизненные пока планеты.<br><br>
    И начнем с Марса!<br><br>
    Присоединяйся!'''


@app.route('/image_mars')
def image_mars():
    return render_template('image_mars.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
