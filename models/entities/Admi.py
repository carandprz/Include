# models/entities/Admi.py
from flask_login import UserMixin

class Admi(UserMixin):
    def __init__(self, username, password, name=None):
        self.username = username
        self.name = name
        self.password = password
    
    def get_id(self):
        return str(self.username)  # Necesario para Flask-Login
