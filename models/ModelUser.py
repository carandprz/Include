#metodo del usuario (user)
from .entities.User import User
import database as db

class ModelUser():
    
    @classmethod
    def login(cls, db, user):
        try:
            cursor = db.database.cursor()
            sql = "SELECT * FROM usuarios WHERE id_usuario = %s"
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()
            if row is not None:
                user_db = User(row[0], row[4])
                if user.password == user_db.password: # verifica contraseña
                    return user_db
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
