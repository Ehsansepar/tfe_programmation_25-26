import json

SAVE_FILE = 'save.json'

def lire():
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"users": {}}

def ecrire(data):
    with open(SAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def register_user(username, password):
    data = lire()
    if username in data["users"]:
        return False
    
    data["users"][username] = {
        "password": password,
        "niveau_debloque": 1
    }
    ecrire(data)
    return True

def login_user(username, password):
    data = lire()
    user = data["users"].get(username)
    if user and user["password"] == password:
        return True
    return False

def get_user_data(username):
    data = lire()
    return data["users"].get(username, None)

def update_niveau(username, nouveau_niveau):
    data = lire()
    user = data["users"].get(username)
    if user:
        if nouveau_niveau > user.get("niveau_debloque", 1):
            user["niveau_debloque"] = nouveau_niveau
            ecrire(data)

