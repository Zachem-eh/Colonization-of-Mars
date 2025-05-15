from flask import Blueprint, make_response, request
from data import db_session
from data.jobs import Jobs
from flask import jsonify
from data.users import User

blueprint = Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs')
def get_jobs():
    sess = db_session.create_session()
    jobs_list = sess.query(Jobs).all()
    return jsonify({
        'jobs': [job.to_dict(only=('id', 'user.name', 'job', 'work_size', 'collaborators',
                                   'start_date', 'end_date', 'is_finished')) for job in jobs_list]
    })


@blueprint.route('/api/jobs/<int:jobs_id>')
def get_jobs_id(jobs_id):
    sess = db_session.create_session()
    job = sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if not job:
        return make_response(jsonify({'status': 'Not found'}, 404))
    return jsonify({ 'job': job.to_dict(only=('id', 'user.name', 'job', 'work_size', 'collaborators',
                                              'start_date', 'end_date', 'is_finished'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    column = ['team_leader', 'job', 'collaborators', 'work_size', 'is_finished']
    if not all([key in column for key in request.json]):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    sess = db_session.create_session()
    jobs = Jobs()
    jobs.team_leader = request.json['team_leader']
    jobs.job = request.json['job']
    jobs.collaborators = request.json['collaborators']
    jobs.work_size = request.json['work_size']
    jobs.is_finished = request.json['is_finished']
    sess.add(jobs)
    sess.commit()
    return jsonify({'jobs.id': jobs.id})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    sess = db_session.create_session()
    job = sess.query(Jobs).get(jobs_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    sess.delete(job)
    sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def put_jobs(jobs_id):
    sess = db_session.create_session()
    try:
        if not request.json:
            return make_response(jsonify({'error': 'Bad request'}), 400)

        job = sess.query(Jobs).get(jobs_id)
        if not job:
            return make_response(jsonify({'error': 'Not found'}), 404)

        params = request.json

        required_fields = ['team_leader', 'job', 'collaborators', 'work_size', 'is_finished']
        if all(params[field] is None for field in required_fields):
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        for key, value in params.items():
            if key == "team_leader" and value:
                user = sess.query(User).get(value)
                if not user:
                    return make_response(jsonify({"error": "team_leader not found"}), 400)
                job.team_leader = value
            if key == 'collaborators' and value:
                id_users = [int(x) for x in value.split(', ')]
                for id_user in id_users:
                    user = sess.query(User).get(id_user)
                    if not user:
                        return make_response(jsonify({"error": "collaborator not found"}), 400)
                job.collaborators = value
            elif value:
                setattr(job, key, value)
        sess.commit()
        return jsonify({str(jobs_id): 'changed'})
    except Exception as e:
        sess.rollback()
        return jsonify({'error': str(e)})
    finally:
        sess.close()
