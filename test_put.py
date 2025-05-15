import requests

params = {'collaborators': '2, 3', 'job': 'test api', 'team_leader': 2}
print(requests.put('http://127.0.0.1:8080/api/jobs/1', json=params).json())
