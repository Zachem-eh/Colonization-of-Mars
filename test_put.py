import requests

# правильные запросы
params = {'collaborators': '2, 3', 'job': 'test api', 'team_leader': 2}
print(requests.put('http://127.0.0.1:8080/api/jobs/1', json=params).json())
params = {'job': 'test api 2.0', 'team_leader': 3, 'work_size': 20}
print(requests.put('http://127.0.0.1:8080/api/jobs/1', json=params).json())

# неправильные запросы
params = {}
print(requests.put('http://127.0.0.1:8080/api/jobs/1', json=params).json())
params = {'team_leader': 999}
print(requests.put('http://127.0.0.1:8080/api/jobs/1', json=params).json())
params = {'collaborators': '999, 1000'}
print(requests.put('http://127.0.0.1:8080/api/jobs/1', json=params).json())