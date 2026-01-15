from app.config.database import get_user_collection
from app.core.security import hash_password, verify_password

def create_user(name, email, password, profession):
    user_collection = get_user_collection()
    
    if user_collection.find_one({"email": email}):
        return None

    user = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "profession": profession,
    }

    result = user_collection.insert_one(user)
    return str(result.inserted_id)

def authenticate_user(email, password):
    user_collection = get_user_collection()
    
    user = user_collection.find_one({"email": email})
    if not user:
        return None

    print(f"Authenticating user: {email}, Hashed password in DB: {user['password']}")
    if not verify_password(password, user["password"]):
        return None

    return user
