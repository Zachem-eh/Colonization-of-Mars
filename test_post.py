import requests

# правильный запрос
job = {
    'team_leader': 1,
    'job': 'deployment of residential modules 1 and 2',
    'collaborators': '2, 3',
    'work_size': '15',
    'is_finished': False
}
print(requests.post('http://127.0.0.1:8080/api/jobs', json=job).json())

# запрос без всех ключей
job = {
    'team_leader': 1,
    'job': 'deployment of residential modules 1 and 2'
}
print(requests.post('http://127.0.0.1:8080/api/jobs', json=job).json())

# запрос с пустым объектом
job = dict()
print(requests.post('http://127.0.0.1:8080/api/jobs', json=job).json())

# запрос с полями неправильного типа
job = {
    'team_leader': 'sqlalchemy',
    'job': 'serializer',
    'collaborators': 'не',
    'work_size': 'хочет',
    'is_finished': 'работать'
}
print(requests.post('http://127.0.0.1:8080/api/jobs', json=job).json())
