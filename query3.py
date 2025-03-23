from data.departments import Department
from data import db_session


db_session.global_init('database/mars_explorer.db')

new_dep = Department()
new_dep.title = 'программирование'
new_dep.chief = 1
new_dep.members = '3, 4'
new_dep.email = 'Code@gmail.com'

session = db_session.create_session()
session.add(new_dep)
session.commit()
