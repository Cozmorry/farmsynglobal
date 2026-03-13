import uuid
from datetime import datetime

def generate_id():
    return str(uuid.uuid4())

def timestamp():
    return datetime.utcnow().isoformat()

def response(message="Success", data=None, status=True):
    return {
        "status": status,
        "message": message,
        "data": data
    }

