from werkzeug.security import check_password_hash   
# models/entities/User.py
from flask_login import UserMixin

class User(UserMixin):
    
    def __init__(self, username, password, name=None, lastname=None):
        self.username = username
        self.password = password
        self.name = name  # Almacena el nombre del usuario
        self.lastname = lastname  # Almacena el apellido del usuario
    
    def get_id(self):
        return str(self.username)  # Esto es necesario para Flask-Login

    #contraseña con hash
    #@classmethod
    #def check_password(self,hased_password,password):
    #    return check_password_hash(hased_password,password)