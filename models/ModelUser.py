from models.entities.User import User
import database as db

class ModelUser():
    
    @classmethod
    def login(cls, db_connection, user):
        try:
            cursor = db_connection.cursor()  # Usa 'db_connection' como se espera
            sql = "SELECT * FROM usuarios WHERE id_usuario = %s"
            cursor.execute(sql, (user.username,))
            row = cursor.fetchone()
            if row is not None:
                user_db = User(row[0], row[4], row[1], row[2])
                if user.password == user_db.password:
                    return user_db
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(cls, db, id):
        try:
            cursor = db.database.cursor()  # Usa 'db.database' en lugar de 'db.connection'
            sql = "SELECT id_usuario, nombre, apellido FROM usuarios WHERE id_usuario = %s"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            
            if row is not None:
                return User(row[0], None, row[1], row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

