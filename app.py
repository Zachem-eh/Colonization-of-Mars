from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template('base.html')


@app.route('/index/<title>')
def index(title):
    return render_template('base.html', title=title)


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


@app.route('/promotion_image')
def promotion_image():
    return render_template('promotion_image.html')


@app.route('/astronaut_selection', methods=['GET', 'POST'])
def astronaut_selection():
    if request.method == 'GET':
        return render_template('astronaut_selection.html')
    elif request.method == 'POST':
        print(request.form['surname'])
        print(request.form['name'])
        print(request.form['email'])
        print(request.form['education'])
        print(request.form['profession'])
        print(request.form['motivation'])
        print(request.form['gender'])
        print(request.form['ready'])
        return '<h1>Анкета отправлена</h1>'


@app.route('/training/<prof>')
def training(prof):
    context = {'prof': prof}
    return render_template('training.html', **context)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)