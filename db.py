from tinydb import TinyDB, Query

db = TinyDB('users.json')

User = Query()

def start():
    db.truncate()
    db.insert({'id': 'admin', 'name': 'Admin', 'temperature': 26.0, 'humidity': 45.0, 'light': 350.0, 'image': '/assets/knight.png'})
    db.insert({'id': ' 51 203 31 1', 'name': 'Monkey', 'temperature': 25.0, 'humidity': 50.0, 'light': 400.0, 'image': '/assets/monkey.png'})
    db.insert({'id': ' 179 146 125 2', 'name': 'Goofy', 'temperature': 28.0, 'humidity': 60.0, 'light': 300.0, 'image': '/assets/goofy.png'})

def get(id):
    results = db.search(User.id == id)
    return results