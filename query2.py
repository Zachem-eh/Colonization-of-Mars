from data.jobs import Jobs
from data import db_session
import datetime


db_session.global_init('database/mars_explorer.db')

new_jobs = Jobs()
new_jobs.team_leader = 1
new_jobs.job = 'deployment of residential modules 1 and 2'
new_jobs.work_size = 15
new_jobs.collaborators = '2, 3'
new_jobs.start_date = datetime.datetime.now()
new_jobs.is_finished = False

session = db_session.create_session()
session.add(new_jobs)
session.commit()
