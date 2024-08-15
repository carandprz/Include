from werkzeug.security import check_password_hash   

class User():
    
    def __init__(self,username,password):
        self.username = username
        self.password = password

    #contraseña con hash
    #@classmethod
    #def check_password(self,hased_password,password):
    #    return check_password_hash(hased_password,password)