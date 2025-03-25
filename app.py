from flask import Flask, render_template, request, make_response, session
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import EmailField, BooleanField
from wtforms.validators import DataRequired
from data import db_session
from data.jobs import Jobs
from data.users import User
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from jobs_api import blueprint
from flask_restful import Api
from user_resource import UserResource, UserListResource
from jobs_resource import JobsResource, JobsListResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

api = Api(app)
api.add_resource(UserResource, '/api/v2/users/<int:user_id>')
api.add_resource(UserListResource, '/api/v2/users')
api.add_resource(JobsResource, '/api/v2/jobs/<int:jobs_id>')
api.add_resource(JobsListResource, '/api/v2/jobs')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobsForm(FlaskForm):
    title = StringField("Название работы")
    team_leader = StringField('ID тим лидера')
    work_size = StringField('Продолжительность')
    collaborators = StringField('Участники')
    finished = BooleanField('Завершена?')
    submit = SubmitField('Добавить')


class RegisterForm(FlaskForm):
    login_email = StringField('Login / email')
    password = PasswordField('Password')
    repeat_password = PasswordField('Repeat password')
    surname = StringField('Surname')
    name = StringField('Name')
    age = StringField('Age')
    position = StringField('Position')
    speciality = StringField('Speciality')
    address = StringField('Address')
    submit = SubmitField('Submit')


@app.route('/')
def main_page():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    return render_template('index.html', jobs=jobs)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/choice/<planet_name>')
def choice(planet_name):
    context = {'planet_name': planet_name}
    return render_template('choice.html', **context)


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    context = {
        'nickname': nickname,
        'level': level,
        'rating': rating
    }
    return render_template('results.html', **context)


@app.route('/distribution')
def distribution():
    context = {
        'astronauts': ['Ридли Скотт', "Энди Уир", "Марк Уотни", "Венката Капур", "Тедди Сандерс", "Шон Бин"]
    }
    return render_template('distribution.html', **context)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        user = User()
        user.email = form.login_email.data
        user.hashed_password = form.password.data
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = int(form.age.data)
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        sess.add(user)
        sess.commit()
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/cookie')
def cookie():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1
    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    form = JobsForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = int(form.team_leader.data)
        job.work_size = int(form.work_size.data)
        job.collaborators = form.collaborators.data
        job.is_finished = form.finished.data
        current_user.jobs.append(job)
        sess.merge(current_user)
        sess.commit()
        return redirect('/')
    return render_template('jobs.html', form=form)


@app.route('/table/<gender>/<int:age>')
def table(gender, age):
    return render_template('table.html', gender=gender, age=age)


if __name__ == '__main__':
    db_session.global_init('database/mars_explorer.db')
    app.register_blueprint(blueprint)
    app.run(host='127.0.0.1', port=8080)