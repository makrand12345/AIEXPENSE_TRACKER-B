def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user.get("name", ""),
        "avatar": user.get("avatar", "")
    }
