def format_single_note(
    note_id: int, title: str, content: str, user_id: int, created_at: str
):
    return {
        "note_info": {
            "id": note_id,
            "title": title,
            "content": content,
            "user_id": user_id,
            "created_at": created_at,
        }
    }
    
def format_multiple_notes(self, notes: list):
    return {
        "count": len(notes), 
        "notes": notes
        }
    
def format_single_user(user_id: int, username: str, created_at: str):
    return {
        "user": {
            "id": user_id, 
            "username": username, 
            "created_at": created_at}
        }

def format_multiple_users(users: list):
    return {
        "count": len(users), 
        "users": users
        }
