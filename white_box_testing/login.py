import requests

session = requests.Session()


data = {
    'email': 'elkin@gmail.com',
    'password': 'Elkin12356'
}

response = session.post('http://127.0.0.1:5000/login/', data=data)

data = {
    'email': 'juanita@gmail.com',
    'password': 'Juana1234'
}

response = session.post('http://127.0.0.1:5000/login/', data=data)

data = {
    'email': 'elkin@gmail.com',
    'password': 'elkin123'
}

response = session.post('http://127.0.0.1:5000/login/', data=data)

response = session.get('http://127.0.0.1:5000/login/')