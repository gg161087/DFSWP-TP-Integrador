import json
import hashlib

def hashear_password(pwd):
    return hashlib.sha256(str(pwd).encode('utf8')).hexdigest()

def validate_user(user, pwd):
    with open('app/files/usuarios.json', 'r') as file:
        users = json.load(file)
        for _user in users:
            if user == _user['user'] and hashear_password(pwd) == _user['pwd']:
                return True
        else:
            return False

def register_user(data):
    with open('app/files/usuarios.json', 'r') as file:
        users_list = json.load(file)
    if not users_list:
        new_id = 1
    else:
        new_id = int(max(users_list, key=lambda x:x['id'])['id']) + 1
    data['id'] = new_id
    users_list.append(data)
    with open('app/files/usuarios.json', 'w') as archivo:
        json.dump(users_list, file, indent = 4)

def get_users():
    with open('app/files/usuarios.json', 'r') as file:
        users = json.load(file)    
    
    return users

def register_person(data):
    with open('app/files/personas.json', 'r') as file:
        peoples_list = json.load(file)
    if not peoples_list:
        new_id = 1        
    else:
        new_id = int(max(peoples_list, key=lambda x:x['id'])['id']) + 1
    data['id'] = new_id    
    peoples_list.append(data)   
       
    with open('app/files/personas.json', 'w') as archivo:
        json.dump(peoples_list, archivo, indent = 4)

def get_people():
    with open('app/files/personas.json', 'r') as file:
        people = json.load(file)    
    
    return people

def get_person(person_id):
    with open('app/files/personas.json', 'r') as file:
        people = json.load(file)
        for person in people:
            if person['id'] == person_id:
                return person
        return None

def delet_person(person_id):
    person_id = int(person_id)
    data = []
    with open('app/files/personas.json', 'r') as file:
        people = json.load(file)
        for person in people:
            if person['id'] != person_id:
                data.append(person)
    with open('app/files/personas.json', 'w') as file:
        json.dump(data, file, indent = 4)

def edit_person(person):    
    with open('app/files/personas.json', 'w') as file:
        file.append(person)
        json.dump(file, indent = 4)