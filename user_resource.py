from flask_restful import Resource, reqparse
from data.db_session import create_session
from data.users import User
from flask import jsonify, abort

parcer = reqparse.RequestParser()
parcer.add_argument('surname', required=False)
parcer.add_argument('name', required=False)
parcer.add_argument('age', required=False, type=int)
parcer.add_argument('position', required=False)
parcer.add_argument('speciality', required=False)
parcer.add_argument('address', required=False)
parcer.add_argument('email', required=False)
parcer.add_argument('hashed_password', required=False)


# /api/users/<id>
class UserResource(Resource):
    def get(self, user_id):
        sess = create_session()
        user = sess.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, 'not found')
        return user.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                  'speciality', 'address', 'email', 'hashed_password'))

    def delete(self, user_id):
        sess = create_session()
        user = sess.query(User).filter(User.id == user_id).first()
        if not user:
            abort(404, 'not found')
        sess.delete(user)
        sess.commit()
        return jsonify({'status': 'ok'})


class UserListResource(Resource):
    def get(self):
        sess = create_session()
        users = sess.query(User).all()
        return jsonify([user.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                           'speciality', 'address', 'email', 'hashed_password')) for user in users])

    def post(self):
        args = parcer.parse_args()
        sess = create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )
        sess.add(user)
        sess.commit()
        return jsonify({'user_id': user.id})