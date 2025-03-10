from data.users import User
from data import db_session

db_session.global_init('database/mars_explorer.db')

capitan = User()
capitan.surname = 'Scott'
capitan.name = 'Ridley'
capitan.age = 21
capitan.position = 'captain'
capitan.speciality = 'research engineer'
capitan.address = 'module_1'
capitan.email = 'scott_chief@mars.org'
capitan.hashed_password = 'FNAF'

colonist_1 = User()
colonist_1.surname = 'Илон'
colonist_1.name = 'Маск'
colonist_1.age = 35
colonist_1.position = 'бухгалтер'
colonist_1.speciality = 'спонсор денег'
colonist_1.address = 'модуль ближе к марсу'
colonist_1.email = 'X@.com'
colonist_1.hashed_password = 'Mars!'

colonist_2 = User()
colonist_2.surname = 'Chat'
colonist_2.name = 'GPT'
colonist_2.age = 4
colonist_2.position = 'программист'
colonist_2.speciality = 'управление ПО корабля'
colonist_2.address = 'компьютер'
colonist_2.email = 'OpenAI@.com'
colonist_2.hashed_password = '4o-mini'

colonist_3 = User()
colonist_3.surname = 'Deep'
colonist_3.name = 'Seek'
colonist_3.age = 1
colonist_3.position = 'китайский шпион'
colonist_3.speciality = 'противостояние с Chat-GPT'
colonist_3.address = 'компьютер'
colonist_3.email = 'DeepSeek@.com'
colonist_3.hashed_password = 'наш слоняра'


session = db_session.create_session()
session.add(capitan)
session.add(colonist_1)
session.add(colonist_2)
session.add(colonist_3)
session.commit()
