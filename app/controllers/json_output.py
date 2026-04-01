def format_single_note(
    note: dict
):
    return {
        "note_info": {
            "id": note.get("id"),
            "title": note.get("title"),
            "content": note.get("content"),
            "user_id": note.get("user_id"),
            "created_at": note.get("created_at"),
        }
    }
    
def format_multiple_notes(notes: list):
    return {
        "count": len(notes), 
        "notes": notes
        }
    
def format_single_user(user: dict):
    return {
        "user": {
            "id": user.get("id"), 
            "username": user.get("username"), 
            "created_at": user.get("created_at")}
        }

def format_multiple_users(users: list):
    return {
        "count": len(users), 
        "users": users
        }
