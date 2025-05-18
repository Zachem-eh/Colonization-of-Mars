import requests
from flask import Flask, render_template, request, make_response, session
from flask_wtf import FlaskForm
from werkzeug.utils import redirect, secure_filename
from wtforms import StringField, PasswordField, SubmitField, FileField, IntegerField
from wtforms.fields.simple import EmailField, BooleanField
from wtforms.validators import DataRequired
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.departments import Department
from data.hazards import Hazard
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from jobs_api import blueprint
from users_api import blueprint_user
from flask_restful import Api
from user_resource import UserResource, UserListResource
from jobs_resource import JobsResource, JobsListResource
import os
import json

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

img = False
if len(os.listdir('static/images/load_photo')) >= 2:
    for f in os.listdir('static/images/load_photo'):
        if f != '.gitkeep':
            img = f
print(img)

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
    hazard_category = StringField('Категория работы')
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
    city_from = StringField('City')
    submit = SubmitField('Submit')


class LoadPhotoForm(FlaskForm):
    cover = FileField('Приложите фотографию',
                      validators=[DataRequired()],
                      render_kw={'accept': 'image/*'})
    submit = SubmitField('Отправить')


class DepartmentsForm(FlaskForm):
    title = StringField("Название департамента", validators=[DataRequired()])
    chief = IntegerField('ID шефа', validators=[DataRequired()])
    members = StringField('Участники', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Добавить')


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
        user.city_from = form.city_from.data
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
        user = sess.merge(current_user)
        hazard = sess.query(Hazard).filter(Hazard.id == int(form.hazard_category.data)).first()
        job = Jobs()
        job.job = form.title.data
        job.team_leader = int(form.team_leader.data)
        job.work_size = int(form.work_size.data)
        job.collaborators = form.collaborators.data
        job.is_finished = form.finished.data
        job.hazard_category = int(form.hazard_category.data)

        user.jobs.append(job)
        hazard.jobs.append(job)
        sess.commit()
        return redirect('/')
    return render_template('jobs.html', form=form)


@app.route('/redactor_jobs/<int:jobs_id>', methods=['GET', 'POST'])
@login_required
def redactor_jobs(jobs_id):
    form = JobsForm()
    sess = db_session.create_session()
    curr_jobs = sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if form.validate_on_submit() and (current_user.id == curr_jobs.team_leader or current_user.id == 1):
        if not sess.query(User).filter(User.id == int(form.team_leader.data)).first():
            return render_template('redactor_jobs.html', form=form, message="Такого тимлида нет")
        users_id = [int(x) for x in form.collaborators.data.split(', ')]
        for user_id in users_id:
            if not sess.query(User).filter(User.id == user_id).first():
                return render_template('redactor_jobs.html', form=form, message="Такого юзера нет")
        curr_jobs.job = form.title.data
        curr_jobs.team_leader = int(form.team_leader.data)
        curr_jobs.work_size = int(form.work_size.data)
        curr_jobs.collaborators = form.collaborators.data
        curr_jobs.is_finished = form.finished.data
        curr_jobs.hazard_category = int(form.hazard_category.data)
        sess.commit()
        return redirect('/')
    form.title.data = curr_jobs.job
    form.team_leader.data =  curr_jobs.team_leader
    form.work_size.data = curr_jobs.work_size
    form.collaborators.data = curr_jobs.collaborators
    form.finished.data = curr_jobs.is_finished
    form.hazard_category.data = curr_jobs.hazard_category
    return render_template('redactor_jobs.html', form=form)


@app.route('/delete_jobs/<int:jobs_id>', methods=['GET', 'DELETE'])
@login_required
def delete_jobs(jobs_id):
    sess = db_session.create_session()
    curr_jobs = sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if curr_jobs and (current_user.id == curr_jobs.team_leader or current_user.id == 1):
        sess.delete(curr_jobs)
        sess.commit()
    return redirect('/')


@app.route('/table/<gender>/<int:age>')
def table(gender, age):
    return render_template('table.html', gender=gender, age=age)


@app.route('/load_photo', methods=['GET', 'POST'])
def load_photo():
    global img
    form = LoadPhotoForm()
    if form.validate_on_submit():
        if img:
            os.remove(f'static/images/load_photo/{img}')
        file = form.cover.data
        filename = secure_filename(file.filename)
        save_path = os.path.join('static/images/load_photo', filename)
        file.save(save_path)
        img = filename
        return redirect('/load_photo')
    return render_template('load_photo.html', form=form, img=img)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    data_user = requests.get(f'http://127.0.0.1:8080/api/users/{user_id}').json()
    sess = db_session.create_session()
    user = sess.query(User).get(user_id)
    url = 'https://geocode-maps.yandex.ru/1.x'
    params = {
        'apikey': '957cd94a-71cc-4433-8fbf-279c95c506aa',
        'geocode': data_user['user']['city_from'],
        'lang': 'ru_RU',
        'format': 'json'
    }
    map_flag = False
    response = requests.get(url=url, params=params)
    if response:
        data = response.json()
        feature = data['response']['GeoObjectCollection']['featureMember']
        if feature:
            pos = ','.join(feature[0]['GeoObject']['Point']['pos'].split())
            url = 'https://static-maps.yandex.ru/v1'
            params = {
                'apikey': 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13',
                'll': pos,
                'spn': '0.16457,0.1619'
            }

            response = requests.get(url, params)
            if response:
                with open(f'static/images/map_{user_id}.png', mode='wb') as map_file:
                    map_file.write(response.content)
                map_flag = True
                user.city_img = f'images/map_{user_id}.png'
                sess.commit()
    return render_template('users_show.html', flag=map_flag, user=user)


@app.route('/member')
def member():
    with open('templates/members.json', mode='r', encoding='utf-8') as json_file:
        members = json.load(json_file)['members']
    return render_template('member.html', members=members)


@app.route('/departments')
def departments():
    sess = db_session.create_session()
    deps = sess.query(Department).all()
    return render_template('departments.html', departments=deps)


@app.route('/add_dep', methods=['GET', 'POST'])
def add_dep():
    form = DepartmentsForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        dep = Department()
        dep.title = form.title.data
        dep.chief = int(form.chief.data)
        dep.members = form.members.data
        dep.email = form.email.data
        sess.add(dep)
        sess.commit()
        return redirect('/departments')
    return render_template('add_dep.html', form=form)


@app.route('/delete_dep/<int:dep_id>', methods=['DELETE', 'GET'])
def delete_dep(dep_id):
    sess = db_session.create_session()
    curr_dep = sess.query(Department).filter(Department.id == dep_id).first()
    if curr_dep and (current_user.id == curr_dep.chief or current_user.id == 1):
        sess.delete(curr_dep)
        sess.commit()
    return redirect('/departments')


@app.route('/redactor_dep/<int:dep_id>', methods=['GET', 'POST'])
def redactor_dep(dep_id):
    form = DepartmentsForm()
    sess = db_session.create_session()
    curr_dep = sess.query(Department).filter(Department.id == dep_id).first()
    if form.validate_on_submit() and (current_user.id == curr_dep.chief or current_user.id == 1):
        if not sess.query(User).filter(User.id == int(form.chief.data)).first():
            return render_template('redactor_dep.html', form=form, message="Такого шефа нет")
        users_id = [int(x) for x in form.members.data.split(', ')]
        for user_id in users_id:
            if not sess.query(User).filter(User.id == user_id).first():
                return render_template('redactor_dep.html', form=form, message="Такого юзера нет")
        curr_dep.title = form.title.data
        curr_dep.chief = int(form.chief.data)
        curr_dep.members = form.members.data
        curr_dep.email = form.email.data
        sess.commit()
        return redirect('/departments')
    form.title.data = curr_dep.title
    form.chief.data = curr_dep.chief
    form.members.data = curr_dep.members
    form.email.data = curr_dep.email
    return render_template('redactor_dep.html', form=form)


if __name__ == '__main__':
    db_session.global_init('database/mars_explorer.db')
    app.register_blueprint(blueprint)
    app.register_blueprint(blueprint_user)
    app.run(host='127.0.0.1', port=8080)