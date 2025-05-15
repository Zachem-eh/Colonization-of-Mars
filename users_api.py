from flask import Blueprint, make_response, request
from data import db_session
from flask import jsonify
from data.users import User

blueprint_user = Blueprint('users_api', __name__, template_folder='templates')


@blueprint_user.route('/api/users')
def get_jobs():
    sess = db_session.create_session()
    users_list = sess.query(User).all()
    return jsonify({
        'users': [user.to_dict(only=('id', 'name', 'surname', 'age', 'position',
                                     'speciality', 'address', 'email')) for user in users_list]
    })


@blueprint_user.route('/api/users/<int:user_id>')
def get_jobs_id(user_id):
    sess = db_session.create_session()
    user = sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'status': 'Not found'}), 404)
    return jsonify({ 'job': user.to_dict(only=('id', 'name', 'surname', 'age', 'position',
                                              'speciality', 'address', 'email'))})


@blueprint_user.route('/api/users', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    column = ['name', 'surname', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password']
    if not all([key in column for key in request.json]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    sess = db_session.create_session()
    user = User()
    params = request.json
    for key, value in params.items():
        if key == 'email':
            check_user = sess.query(User).filter(User.email == value).first()
            if check_user:
                return make_response(jsonify({'error': 'email уже занят'}), 400)
            user.email = value
        else:
            setattr(user, key, value)
    sess.add(user)
    sess.commit()
    return jsonify({'jobs.id': user.id})


@blueprint_user.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_jobs(user_id):
    sess = db_session.create_session()
    user = sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    sess.delete(user)
    sess.commit()
    return jsonify({'success': 'OK'})


@blueprint_user.route('/api/users/<int:user_id>', methods=['PUT'])
def put_jobs(user_id):
    sess = db_session.create_session()
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Bad request'}), 400)

        user = sess.query(User).get(user_id)
        if not user:
            return make_response(jsonify({'error': 'Not found'}), 404)

        params = request.json

        for key, value in params.items():
            if key == 'email' and value:
                check_user = sess.query(User).filter(User.email == value).first()
                if check_user:
                    return make_response(jsonify({'error': 'email уже занят'}), 400)
                user.email = value
            if value:
                setattr(user, key, value)
        sess.commit()
        return jsonify({str(user_id): 'changed'})
    except Exception as e:
        sess.rollback()
        return jsonify({'error': str(e)})
    finally:
        sess.close()
