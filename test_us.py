import requests

# правильные запросы
print(requests.get('http://127.0.0.1:8080/api/users/1').json())
print(requests.get('http://127.0.0.1:8080/api/users').json())
print(requests.delete('http://127.0.0.1:8080/api/users/1').json())
user = {'surname': 'surname', 'name': 'name', 'age': 1, 'position': 'position',
        'speciality': 'speciality',
        'address': 'address',
        'email': 'email@.com',
        'hashed_password': 'hashed_password'}
print(requests.post('http://127.0.0.1:8080/api/users', json=user).json())

# get с неправильным запросом
print(requests.get('http://127.0.0.1:8080/api/users/999').json())

# delete с неправильным запросом
print(requests.delete('http://127.0.0.1:8080/api/users/999').json())

# post с неправильным запросом
user = dict()
print(requests.post('http://127.0.0.1:8080/api/users', json=user).json())