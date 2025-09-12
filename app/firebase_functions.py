from app.firebase_init import firestore_init

db = firestore_init()

def f_add_user(uid: str, email: str, first_name: str, last_name: str,
             reg_no: str, cgpa: float, branch: str,
             passing_year: int, marks_10th: float, marks_12th: float,
             placement_drive_info: dict):
    """
    Add or update a user with academic + placement details in Firestore.
    """
    
    user_data = {
        "uid": uid,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "reg_no" : reg_no,
        "cgpa": cgpa,
        "branch": branch,
        "passing_year": passing_year,
        "marks_10th": marks_10th,
        "marks_12th": marks_12th,
        "placement_drive_info": placement_drive_info
    }
    db.collection("users").document(uid).set(user_data)
    print(f"✅ User {uid} added/updated.")


def f_get_user(uid: str):
    """
    Retrieve a user's data by UID.
    """
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        return doc.to_dict()
    else:
        print(f"User {uid} not found.")
        return None

def f_get_branches():
    """
    Retreive all the Department Branches
    """
    docs = db.collection("branches").stream()
    return [doc.to_dict()["name"] for doc in docs]


if __name__ == "__main__":
    print(f_get_branches())

