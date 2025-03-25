import requests

# правильные запросы
print(requests.get('http://127.0.0.1:8080/api/v2/jobs/1').json())
print(requests.get('http://127.0.0.1:8080/api/v2/jobs').json())
print(requests.delete('http://127.0.0.1:8080/api/v2/jobs/1').json())
job = {'team_leader': 1, 'job': 'job', 'work_size': 10, 'collaborators': '1, 2', 'is_finished': False}
print(requests.post('http://127.0.0.1:8080/api/v2/jobs', json=job).json())

# get с неправильным запросом
print(requests.get('http://127.0.0.1:8080/api/v2/jobs/999').json())

# delete с неправильным запросом
print(requests.delete('http://127.0.0.1:8080/api/v2/jobs/999').json())

# post с неправильным запросом
job = dict()
print(requests.post('http://127.0.0.1:8080/api/v2/jobs', json=job).json())
