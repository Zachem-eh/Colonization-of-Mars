from flask_restful import Resource, reqparse
from data.db_session import create_session
from data.jobs import Jobs
from flask import jsonify, abort

parcer = reqparse.RequestParser()
parcer.add_argument('team_leader', required=False, type=int)
parcer.add_argument('job', required=False)
parcer.add_argument('work_size', required=False, type=int)
parcer.add_argument('collaborators', required=False)
parcer.add_argument('is_finished', required=False, type=bool)


# /api/jobs/<id>
class JobsResource(Resource):
    def get(self, jobs_id):
        sess = create_session()
        job = sess.query(Jobs).filter(Jobs.id == jobs_id).first()
        if not job:
            abort(404, 'not found')
        return job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished'))

    def delete(self, jobs_id):
        sess = create_session()
        job = sess.query(Jobs).filter(Jobs.id == jobs_id).first()
        if not job:
            abort(404, 'not found')
        sess.delete(job)
        sess.commit()
        return jsonify({'status': 'ok'})


class JobsListResource(Resource):
    def get(self):
        sess = create_session()
        users = sess.query(Jobs).all()
        return jsonify([user.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished'))
                        for user in users])

    def post(self):
        args = parcer.parse_args()
        sess = create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        sess.add(job)
        sess.commit()
        return jsonify({'jobs_id': job.id})