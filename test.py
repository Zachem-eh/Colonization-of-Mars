import requests

print(requests.get('http://127.0.0.1:8080/api/jobs').json())
print(requests.get('http://127.0.0.1:8080/api/jobs/1').json())
print(requests.get('http://127.0.0.1:8080/api/jobs/666').json())
print(requests.get('http://127.0.0.1:8080/api/jobs/serializer_живи').json())
