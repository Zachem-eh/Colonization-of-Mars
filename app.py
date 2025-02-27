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


@app.route('/astronaut_selection')
def astronaut_selection():
    return render_template('astronaut_selection.html')

@app.route('/answer', methods=['POST'])
@app.route('/auto_answer', methods=['POST'])
def answer():
    context ={
        'title': 'Анкета',
        'surname': request.form['surname'],
        'name': request.form['name'],
        'education': request.form['education'],
        'profession': ', '.join(request.form.getlist('profession')),
        'gender': request.form['gender'],
        'motivation': request.form['motivation'],
        'ready': request.form.get('ready', '') == 'Готов'
    }
    return render_template('answer.html', **context)


@app.route('/training/<prof>')
def training(prof):
    context = {'prof': prof}
    return render_template('training.html', **context)


@app.route('/list_prof/<lst>')
def list_prof(lst):
    context = {
        'list': lst,
        'profs': ['врач', "инженер", "пилот", "биолог", "метеоролог"]
    }
    return render_template('list_prof.html', **context)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)